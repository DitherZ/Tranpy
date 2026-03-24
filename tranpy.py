#!/usr/bin/env python3

# ─────[TranPy]────────────────────────────────────────────────────────────────
# Advanced Document Translation Tool
# Author: DitherZ (Kali Linux Rolling 2026.1)
# Description: Multi-format document translation with intelligent batch processing
#              Supports PDF, DOCX, TXT, and URL inputs with automatic language detection
#              Features async translation, smart caching, and robust error handling
#              Optimized for large documents with progress tracking and logging
# ──────────────────────────────────────────────────────────────────────────────

# ──── IMPORTS ──── #

import os
import re
import sys
import time
import argparse
import logging
import datetime
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache, wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import signal

from tqdm import tqdm
from deep_translator import GoogleTranslator
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import aiohttp


# ──── ANSI DEFINITIONS ──── #

BOLD = "\033[1m"
ITL = "\033[3m"
DIM = "\033[2m"
RVRS = "\033[7m"
BLINK = "\033[5m"
RESET = "\033[0m"
RC = "\033[0m"
RCFG = "\033[39m"
RCBG = "\033[49m"
RCFX = "\033[22m"

GRN = "\033[0;38;5;40m"
AMB = "\033[0;38;5;214m"
BLU = "\033[0;38;5;74m"
MAG = "\033[0;38;5;165m"
RED = "\033[0;38;5;196m"
SKY = "\033[0;38;5;111m"
WHT = "\033[0;38;5;231m"
LGRAY = "\033[0;38;5;250m"
DGRAY = "\033[0;38;5;240m"

WHT_BG = "\033[48;5;231m"
DGRAY_BG = "\033[48;5;240m"

WFG_BBG = "\033[0;1;38;5;233;48;5;255m"
SKYFG_GBG = "\033[0;1;38;5;111;48;5;240m"
GRNFG_GBG = "\033[0;1;38;5;40;48;5;240m"
BLUFG_GBG = "\033[0;1;38;5;74;48;5;240m"
AMBFG_GBG = "\033[0;1;38;5;214;48;5;240m"
REDFG_GBG = "\033[0;1;38;5;196;48;5;240m"

def print_info(msg): print(f"\n{SKYFG_GBG}  INFO  {SKY} {msg}{RC}")
def print_task(msg): print(f"\n{BLUFG_GBG}  TASK  {BLU} {msg}{RC}")
def print_done(msg): print(f"\n{GRNFG_GBG}  DONE  {GRN} {msg}{RC}")
def print_warn(msg): print(f"\n{AMBFG_GBG}  WARN  {AMB} {msg}{RC}")
def print_fail(msg): print(f"\n{REDFG_GBG}  FAIL  {RED} {msg}{RC}")
def print_filepath(msg): print(f"{ITL}{SKY}{msg}{RC}")


# ───────────────────────── CONFIGURATION ───────────────────────── #

DEFAULT_LOG_DIR = Path.home() / ".log" / "tranpy"
DEFAULT_OUTPUT_DIR = Path.home() / "tranpy" / "Translated_Docs"
DEFAULT_TIMEOUT = 15
DEFAULT_BATCH_SIZE = 20
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_WORKERS = 4
TARGET_LANG = "en"
CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]+')
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md', '.rst'}


# ───────────────────────── LOGGING SETUP ───────────────────────── #

def setup_logging(log_dir: Path):
    """Configure logging with rotation and proper formatting."""
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"tranpy_{timestamp}.log"

    # Use RotatingFileHandler to prevent log file from growing too large
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    print_info("Logging initialised")
    print_filepath(str(log_path))
    return logger


# ───────────────────────── NETWORK SESSION ───────────────────────── #

def build_session(timeout: int = DEFAULT_TIMEOUT) -> requests.Session:
    """Create a session with optimized connection pooling."""
    session = requests.Session()
    
    # Configure retry strategy with exponential backoff
    retry_strategy = Retry(
        total=DEFAULT_MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    
    # Configure connection pooling
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=20
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set default timeout
    session.timeout = timeout
    
    return session


# ───────────────────────── FILE EXTRACTION ───────────────────────── #

def extract_input(source: str, max_size: int = 50 * 1024 * 1024) -> str:
    """
    Extract text from various input types with size validation.
    
    Args:
        source: File path, URL, or direct text
        max_size: Maximum file size to process (default 50MB)
    
    Returns:
        Extracted text content
    """
    path = Path(source)
    
    if path.exists():
        # Check file size
        if path.stat().st_size > max_size:
            raise ValueError(f"File too large: {path.stat().st_size} > {max_size} bytes")
        
        suffix = path.suffix.lower()
        
        if suffix == ".pdf":
            print_task("Extracting PDF content")
            try:
                return extract_pdf_text(str(source))
            except Exception as e:
                raise RuntimeError(f"PDF extraction failed: {e}")
        
        if suffix == ".docx":
            print_task("Extracting DOCX content")
            try:
                doc = Document(source)
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                raise RuntimeError(f"DOCX extraction failed: {e}")
        
        # Handle text-based files
        if suffix in SUPPORTED_EXTENSIONS:
            return path.read_text(encoding="utf-8")
        else:
            print_warn(f"Unsupported file type: {suffix}, attempting to read as text")
            return path.read_text(encoding="utf-8", errors="ignore")
    
    return source


# ───────────────────────── TRANSLATION CORE ───────────────────────── #

class TranslationCache:
    """Enhanced cache with TTL and size limits."""
    
    def __init__(self, maxsize: int = 5000, ttl: int = 3600):
        self.cache = {}
        self.maxsize = maxsize
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[str]:
        """Get cached translation if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: str):
        """Set cached translation with timestamp."""
        if len(self.cache) >= self.maxsize:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()


# Global translator instance with cache
_translator_cache = TranslationCache()

def cached_translate(text: str, target: str) -> str:
    """Translate with caching to avoid redundant API calls."""
    # Create cache key
    cache_key = hashlib.md5(f"{text}:{target}".encode()).hexdigest()
    
    # Check cache
    cached = _translator_cache.get(cache_key)
    if cached:
        return cached
    
    # Perform translation
    translator = GoogleTranslator(source='auto', target=target)
    result = translator.translate(text)
    
    # Cache result
    _translator_cache.set(cache_key, result)
    
    return result


def translate_text(text: str, target: str, batch_size: int) -> str:
    """
    Translate text with batched processing and progress tracking.
    
    Args:
        text: Input text to translate
        target: Target language code
        batch_size: Number of lines per batch
    
    Returns:
        Translated text
    """
    lines = text.splitlines()
    output_lines = []
    
    # Use a context manager for tqdm
    with tqdm(
        total=len(lines),
        desc=f"Translating to {target}",
        unit="line",
        ncols=80
    ) as pbar:
        for i in range(0, len(lines), batch_size):
            batch = lines[i:i + batch_size]
            batch_text = "\n".join(batch)
            
            # Skip if no CJK characters
            if not CJK_PATTERN.search(batch_text):
                output_lines.extend(batch)
                pbar.update(len(batch))
                continue
            
            try:
                translated_batch = cached_translate(batch_text, target)
                output_lines.extend(translated_batch.splitlines())
                pbar.update(len(batch))
            except Exception as e:
                print_warn(f"Translation failed for batch {i//batch_size + 1}: {e}")
                output_lines.extend(batch)
                pbar.update(len(batch))
    
    return "\n".join(output_lines)


# ───────────────────────── ASYNC SUPPORT ───────────────────────── #

async def translate_text_async(text: str, target: str, batch_size: int) -> str:
    """Asynchronous version of translate_text."""
    lines = text.splitlines()
    output_lines = []
    semaphore = asyncio.Semaphore(5)  # Limit concurrent API calls
    
    async def translate_batch(batch_text: str) -> List[str]:
        """Translate a single batch with rate limiting."""
        async with semaphore:
            # Run blocking translation in thread pool
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(
                    executor, cached_translate, batch_text, target
                )
            return result.splitlines()
    
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        batch_text = "\n".join(batch)
        
        if not CJK_PATTERN.search(batch_text):
            output_lines.extend(batch)
            continue
        
        try:
            translated = await translate_batch(batch_text)
            output_lines.extend(translated)
        except Exception as e:
            print_warn(f"Async translation failed: {e}")
            output_lines.extend(batch)
    
    return "\n".join(output_lines)


# ───────────────────────── EXECUTION CORE ───────────────────────── #

class TimeoutError(Exception):
    """Custom timeout exception."""
    pass

@contextmanager
def timeout(seconds: int):
    """Context manager for timeout."""
    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")
    
    # Set timeout handler
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


def run_translation(source: str, args):
    """Main translation execution with improved error handling."""
    session = build_session()
    counters = {"success": 0, "failed": 0}
    start_time = time.time()
    
    try:
        # Input extraction with timeout
        print_task("Extracting input")
        with timeout(30):  # 30 second timeout for extraction
            if source.startswith(("http://", "https://")):
                response = session.get(source)
                response.raise_for_status()
                input_text = response.text
            else:
                input_text = extract_input(source)
        
        total_lines = len(input_text.splitlines())
        print_info(f"Processing {total_lines} lines")
        
        # Process each target language
        for target in args.targets:
            print_task(f"Translating → {target}")
            
            # Use async if specified
            if args.async_mode:
                translated_text = asyncio.run(
                    translate_text_async(input_text, target, args.batch_size)
                )
            else:
                translated_text = translate_text(
                    input_text, target=target, batch_size=args.batch_size
                )
            
            # Generate output path
            if args.hash_names:
                digest = hashlib.sha256(input_text.encode()).hexdigest()[:8]
                output_path = args.output_dir / f"{digest}_{target}.txt"
            else:
                name = Path(source).stem if Path(source).exists() else "translated_text"
                output_path = args.output_dir / f"{name}_{target}.txt"
            
            # Ensure output directory exists
            args.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Write output with backup
            if output_path.exists() and not args.force_overwrite:
                backup_path = output_path.with_suffix(f".bak{output_path.suffix}")
                output_path.rename(backup_path)
                print_warn(f"Backup created: {backup_path}")
            
            output_path.write_text(translated_text, encoding="utf-8")
            
            counters["success"] += 1
            print_done(f"Completed → {target}")
            print_filepath(str(output_path))
            
            # Log file size
            file_size = output_path.stat().st_size
            print_info(f"Output size: {file_size:,} bytes")
    
    except TimeoutError as e:
        counters["failed"] += 1
        print_fail(f"Operation timed out: {e}")
        logging.exception("Timeout error")
    except requests.RequestException as e:
        counters["failed"] += 1
        print_fail(f"Network error: {e}")
        logging.exception("Network error")
    except Exception as e:
        counters["failed"] += 1
        print_fail(str(e))
        logging.exception("Unexpected error")
    finally:
        session.close()
    
    # Performance metrics
    end_time = time.time()
    duration = end_time - start_time
    throughput = total_lines / duration if duration > 0 else 0
    
    print_info(f"Duration: {duration:.2f}s | Throughput: {throughput:.2f} lines/sec")
    print_info(f"Success: {counters['success']} | Failed: {counters['failed']}")


# ───────────────────────── CLI INTERFACE ───────────────────────── #

def main():
    parser = argparse.ArgumentParser(
        description="TRANPY Extended - Advanced Document Translation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.txt -t es fr de
  %(prog)s https://example.com/article.html -t zh
  %(prog)s document.pdf --batch-size 15 --hash-names
  %(prog)s document.docx --async-mode --force-overwrite
        """
    )
    
    parser.add_argument("source", help="Text, file path, or URL")
    parser.add_argument("-t", "--targets", nargs="+", default=[TARGET_LANG],
                       help=f"Target language codes (default: {TARGET_LANG})")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE,
                       help=f"Lines per translation batch (default: {DEFAULT_BATCH_SIZE})")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR,
                       help="Directory for log files")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                       help="Directory for translated files")
    parser.add_argument("--hash-names", action="store_true",
                       help="Use content hash for output filenames")
    parser.add_argument("--force-overwrite", action="store_true",
                       help="Overwrite existing output files")
    parser.add_argument("--async-mode", action="store_true",
                       help="Use async translation for better performance")
    parser.add_argument("--no-progress", action="store_true",
                       help="Disable progress bars")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure progress bars
    if args.no_progress:
        tqdm.disable = True
    
    # Configure logging
    logger = setup_logging(args.log_dir)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Run translation
    run_translation(args.source, args)


if __name__ == "__main__":
    main()
