#!/usr/bin/env python3

"""
TranPy - Advanced Document Translation Tool
============================================

Multi-format document translation with intelligent batch processing.
Supports PDF, DOCX, TXT, and URL inputs with automatic language detection.

Features:
---------
- Smart batch processing with CJK character detection
- Asynchronous translation for improved performance
- Persistent caching with TTL to reduce API calls
- Automatic retry with exponential backoff
- Progress tracking with tqdm integration
- Comprehensive logging with rotation
- File size validation and timeout protection
- Backup creation for existing outputs
- Connection pooling for network efficiency

Examples:
---------
    # Translate a file to multiple languages
    tranpy document.txt -t es fr de
    
    # Translate a web page
    tranpy https://example.com/article.html -t zh
    
    # Use async mode for better performance
    tranpy document.pdf --batch-size 15 --async-mode
    
    # Process with hash-based filenames
    tranpy document.docx --hash-names --force-overwrite

Requirements:
------------
Python 3.8+ with packages: deep-translator, pdfminer.six, python-docx,
tqdm, requests, aiohttp, urllib3
"""

__version__ = "2.0.0"
__author__ = "Blackflame"
__license__ = "MIT"
__copyright__ = "Copyright 2026 Blackflame"

from tranpy.tranpy import (
    translate_text,
    translate_text_async,
    extract_input,
    build_session,
    setup_logging,
    run_translation,
    main,
)

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "translate_text",
    "translate_text_async",
    "extract_input",
    "build_session",
    "setup_logging",
    "run_translation",
    "main",
]
