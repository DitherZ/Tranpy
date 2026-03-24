# TranPy - Advanced Document Translation Tool

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)]()

TranPy is a powerful, feature-rich document translation tool designed to handle complex translation tasks with intelligence and efficiency. Built for both casual users and automation workflows, it excels at preserving document structure while delivering accurate translations.

## ✨ Features

### Core Capabilities
- **Multi-Format Support**: Translate PDF, DOCX, TXT, Markdown, and reStructuredText files
- **Web Page Translation**: Convert any URL to translated plain text
- **Batch Processing**: Smart line batching with CJK character detection
- **Multi-Language Output**: Translate to multiple target languages in one run
- **Automatic Language Detection**: Source language auto-detection via Google Translate

### Advanced Features
- **Intelligent Caching**: LRU cache with TTL to minimize API calls and improve performance
- **Async Translation Mode**: Concurrent processing for faster translations on large documents
- **Progress Tracking**: Real-time progress bars with line count tracking
- **Smart Error Handling**: Automatic retries with exponential backoff
- **Comprehensive Logging**: Rotating logs with timestamp tracking
- **File Size Validation**: Prevents processing of excessively large files
- **Backup Creation**: Automatic backup of existing output files
- **Connection Pooling**: Optimized network sessions for better performance

### Performance Optimizations
- **Batch Translation**: Configurable batch sizes for optimal API usage
- **CJK Detection**: Skips non-CJK content to reduce unnecessary API calls
- **Timeout Protection**: Prevents hanging operations with configurable timeouts
- **Memory Management**: Stream processing and cache size limits
- **Throughput Metrics**: Real-time performance statistics

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for translation API access

## 🚀 Installation

### From Source (Recommended)
```bash
# Clone the repository
git clone https://github.com/DitherZ/TranPy.git
cd TranPy

# Install dependencies
pip install -r requirements.txt

# Install the package
python setup.py install
```

Direct Installation

```bash
# Coming soon to PyPI
# pip install tranpy
```

💻 Usage

Basic Usage

```bash
# Translate a text file to Spanish
tranpy document.txt -t es

# Translate to multiple languages
tranpy document.txt -t es fr de zh

# Translate a web page
tranpy https://example.com/article.html -t es
```

Advanced Options

```bash
# Use async mode for better performance on large files
tranpy large_document.pdf --async-mode

# Control batch size for API optimization
tranpy document.txt -t es --batch-size 15

# Use hash-based filenames for better organization
tranpy document.docx --hash-names

# Force overwrite existing files
tranpy document.txt -t es fr --force-overwrite

# Disable progress bars for script integration
tranpy document.txt -t es --no-progress

# Enable verbose logging for debugging
tranpy document.txt -t es --verbose
```

File Format Support

Format Support Notes
PDF ✅ Full Extracts text while preserving structure
DOCX ✅ Full Reads all paragraphs and formatting
TXT ✅ Full Direct text processing
Markdown ✅ Full Preserves markdown structure
reStructuredText ✅ Full Preserves RST structure
URLs ✅ Full Fetches and translates web content

Command Line Arguments

```
positional arguments:
  source                Text, file path, or URL

optional arguments:
  -t, --targets TARGETS [TARGETS ...]
                        Target language codes (default: en)
  --batch-size BATCH_SIZE
                        Lines per translation batch (default: 20)
  --log-dir LOG_DIR     Directory for log files
  --output-dir OUTPUT_DIR
                        Directory for translated files
  --hash-names          Use content hash for output filenames
  --force-overwrite     Overwrite existing output files
  --async-mode          Use async translation for better performance
  --no-progress         Disable progress bars
  --verbose             Enable verbose logging
```

📊 Performance Metrics

TranPy provides real-time performance metrics after each translation:

· Duration: Total processing time
· Throughput: Lines processed per second
· Success/Failure Count: Translation success rate
· Output Size: Size of translated files

🛠️ Development

Project Structure

```
tranpy/
├── __init__.py         # Package initialization
├── tranpy.py           # Main application code
├── setup.py            # Installation configuration
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

Testing

```bash
# Run tests (coming soon)
python -m pytest tests/
```

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Development Setup

```bash
# Clone the repository
git clone https://github.com/DitherZ/TranPy.git
cd TranPy

# Install development dependencies
pip install -e ".[dev]"

# Run code formatting
black tranpy/

# Check code style
flake8 tranpy/

# Type checking
mypy tranpy/
```

📝 License

```text
MIT License

Copyright © 2026 Jason Zarri | DitherZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

🙏 Acknowledgments

· Google Translate for translation services
· deep-translator Python library
· pdfminer.six for PDF processing
· python-docx for DOCX processing
· tqdm for progress bars

📞 Support

· Issues: GitHub Issues
· Discussions: GitHub Discussions

---

Made with ❤️ by DitherZ
Your intelligent document translation companion
