GetGoogleBooks
==============

A Python application to download Google Books to a given folder, and then convert the files into a PDF document that can be read with a PDF viewer. It's actually a mix of pysheng and img2pdf.

**Note**: This application only downloads pages that Google Books makes freely available in preview mode - it won't bypass any access restrictions that Google has in place for specific books.

Requirements
------------

- Python 2.7 or Python 3.x
- Python Imaging Library (PIL) or Pillow
- For Python 2.7: `pip install Pillow==6.2.2`
- For Python 3.x: `pip install Pillow`

The following dependencies are included in this repository:
- img2pdf (GPL licensed)
- PyZenity (GPL licensed) - used by the original GUI version

License
-------

Released under GPL v3.

Usage
-----

### Command Line Interface (Recommended)

Simply run in a terminal:

```bash
python cli.py "GOOGLE_BOOK_URL"
```

Replace `GOOGLE_BOOK_URL` with the full URL of the Google Book you want to download.

### Legacy GUI Interface

The original GUI interface is still available but may require additional setup:

```bash
python download.py
```

This will open dialog boxes to guide you through the process.

### Output

The application will:
1. Create a `BOOKS` directory in your current folder
2. Download all available pages as PNG images to `BOOKS/[Book Title]/`
3. Automatically combine them into a single PDF: `BOOKS/[Book Title].pdf`

### What Gets Downloaded

- Only pages visible in Google Books preview mode
- Typically includes: cover, table of contents, sample chapters, and index pages
- The exact content depends on what Google Books makes freely available for that specific book

Recent Improvements
-------------------

This fork includes several modernization fixes:
- **Cross-platform CLI interface** - Works on Windows, macOS, and Linux without Java dependencies
- **Fixed PIL/Pillow compatibility** - Updated for modern Python imaging libraries
- **Windows command line length handling** - Uses temporary batch files to avoid CMD length limits
- **Modern user-agent string** - Updated to avoid detection/blocking
- **Improved error handling** - Better feedback when operations fail
- **Python 2/3 compatibility improvements** - Fixed deprecated syntax issues

Known Issues
------------

- img2pdf may have issues with some colorspaces, so colorspace is defaulted to monochrome (1-bit). This may affect covers but should render text contents properly.
- The application respects Google's access restrictions and will only download what's freely available in preview mode.

Troubleshooting
---------------

**"ImportError: No module named PIL"**
- Install Pillow: `pip install Pillow` (Python 3) or `pip install Pillow==6.2.2` (Python 2.7)

**"Command line too long" error**
- This has been fixed in the current version using temporary batch files

**"No image found in HTML page"**
- Google Books may have changed their page structure or the book may have restricted access
- Try a different book or check if the book is available in your region

Contributing
------------

This is a fork of the original project. Feel free to submit issues and pull requests for improvements.

Original project: https://github.com/ekianjo/GetGoogleBooks
