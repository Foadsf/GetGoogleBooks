#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cli.py - Cross-platform CLI wrapper for GetGoogleBooks

import sys
import os
import platform
import argparse
from download import download_book, makepdf  # Import core functions from download.py


# Main function (adapted from download.py)
def main():
    parser = argparse.ArgumentParser(
        description="Download Google Books as PDF. Provide the URL as a command-line argument."
    )
    parser.add_argument(
        "url", help="Google Book URL (e.g., https://books.google.com/books?id=EXAMPLE)"
    )  # Required positional arg
    args = parser.parse_args()

    # Print info messages to console (no GUI)
    print(
        "This Application will let you download Google Books available in browser mode in PNG format locally for offline reading"
    )
    print("Note: Using cross-platform CLI—no Java needed!")

    bookurl = args.url

    # Rest of the logic from download.py (download pages and make PDF)
    image_file_template = "%(attribution)s - %(title)s.page-%(page)03d"
    info = None  # To capture info for makepdf
    for info, page, image_data in download_book(bookurl):
        namespace = dict(title=info["title"], attribution=info["attribution"])
        output_file = (
            (image_file_template + ".png") % dict(namespace, page=page + 1)
        ).encode("utf-8")
        if not os.path.isdir("BOOKS"):
            os.mkdir("BOOKS")
        book_dir = os.path.join("BOOKS", info["title"])
        if not os.path.isdir(book_dir):
            os.mkdir(book_dir)
        with open(os.path.join(book_dir, output_file), "wb") as f:
            f.write(image_data)
        print(output_file)

    if info:
        makepdf(os.path.join("BOOKS", info["title"]), info["title"])
    else:
        print("No book info found—download may have failed.")


if __name__ == "__main__":
    # Platform-specific tweaks (if needed)
    if platform.system() == "Windows":
        # No extras needed for CLI
        pass
    main()
