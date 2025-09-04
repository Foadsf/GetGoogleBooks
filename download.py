#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) Arnau Sanchez <tokland@gmail.com>

# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import re, os
import sys
import itertools
from os import listdir
from os.path import isfile, join
import subprocess

try:
    # Python >= 2.6
    import json
except ImportError:
    import simplejson as json

import lib

AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"  # Modern user-agent to avoid detection/blocking

class ParsingError(Exception):
    pass

def get_id_from_string(s):
    """Return book ID from a string (can be a book code or URL)."""
    if "/" not in s:
        return s
    url = s
    match = re.search("[?&]?id=([^&]+)", url)
    if not match:
        raise ParsingError, "Error extracting id query string from URL: %s" % url
    return match.group(1)

def get_cover_url(book_id):
    return "http://books.google.com/books?id=%s&hl=en&printsec=frontcover" % book_id

def get_info(cover_html):
    """Return dictionary with the book info (prefix, page_ids, title, attribution)."""
    tag = lib.first(s for s in cover_html.split("<")
        if re.search('input[^>]*\s+name="?ie"?', s))
    if tag:
        match = re.search('value="(.*?)"', tag)
        if not match:
            raise ParsingError, "Cannot found encoding info"
        encoding = match.group(1).lower()
    else:
        encoding = "iso8859-15"
    match = re.search(r'_OC_Run\((.*?)\);', cover_html)
    if not match:
        raise ParsingError, "No JS function OC_Run() found in HTML"
    oc_run_args = json.loads("[%s]" % match.group(1), encoding=encoding)
    if len(oc_run_args) < 2:
        raise ParsingError, "Expecting at least 2 arguments in function OC_Run()"
    pages_info, book_info = oc_run_args[:2]
    page_ids = [x["pid"] for x in sorted(pages_info["page"], key=lambda d: d["order"])]
    if not page_ids:
        raise ParsingError, "No page_ids found"
    prefix = pages_info["prefix"].decode("raw_unicode_escape")
    return {
        "prefix": prefix,
        "page_ids": page_ids,
        "title": book_info["title"],
        "attribution": re.sub("^By\s+", "", book_info["attribution"]),
    }

def get_image_url_from_page(html):
    """Get image from a page html."""
    if "/googlebooks/restricted_logo.gif" in html:
        return
    match = re.search(r'background-image:url\("([^"]+)"\)', html)  # Updated regex for current Google Books structure
    if not match:
        print("DEBUG: Raw page HTML for inspection:\n" + html)  # Debug print
        raise ParsingError, "No image found in HTML page"
    return match.group(1)

def get_page_url(prefix, page_id):
    return prefix + "&pg=" + page_id

def download(*args, **kwargs):
    return lib.download(*args, **dict(kwargs, agent=AGENT))

def download_book(url, page_start=0, page_end=None):
    """Yield (info, page, image_data) for pages from page_start to page_end"""
    opener = lib.get_cookies_opener()
    cover_url = get_cover_url(get_id_from_string(url))
    cover_html = download(cover_url, opener=opener)
    info = get_info(cover_html)
    page_ids = itertools.islice(info["page_ids"], page_start, page_end)
    for page, page_id in enumerate(page_ids, page_start):
        page_url = get_page_url(info["prefix"], page_id)
        page_html = download(page_url, opener=opener)
        image_url = get_image_url_from_page(page_html)
        if image_url:
          image_data = download(image_url, opener=opener)
          yield info, page, image_data

def makepdf(mypath, title):
    from os import listdir
    from os.path import isfile, join
    import subprocess
    import tempfile
    import os

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.sort()

    # Create a temporary batch file to handle long command lines
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as batch_file:
        batch_path = batch_file.name

        # Build the command in chunks to avoid command line length limits
        cmd_parts = ['python', 'img2pdf.py']

        # Add all image files
        for element in onlyfiles:
            cmd_parts.append('"%s"' % os.path.join(mypath, element))

        # Add output and options
        cmd_parts.extend(['-o', '"BOOKS/%s.pdf"' % title, '-C', '1'])

        # Write the command to the batch file
        batch_file.write(' '.join(cmd_parts))

    print("Created batch file with %d images" % len(onlyfiles))
    print("Command: %s" % ' '.join(cmd_parts[:3] + ['...'] + cmd_parts[-4:]))

    # Execute the batch file
    proc = subprocess.Popen([batch_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    # Clean up the temporary batch file
    try:
        os.unlink(batch_path)
    except:
        pass

    if proc.returncode != 0:
        print("Error creating PDF:")
        if stderr:
            print(stderr.decode('utf-8', errors='ignore'))
    else:
        print("PDF created successfully: BOOKS/%s.pdf" % title)

if __name__ == '__main__':
    # Original main removed, as cli.py handles entry point now
    pass
