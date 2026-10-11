#!/usr/bin/env python3
"""Validate the immutable updater source before invoking the Go linker."""
import json
import re
import sys
from pathlib import Path


def read(path):
    data = json.loads(Path(path).read_text())
    repo = data.get('repository', '')
    if data.get('schema') != 1 or not isinstance(repo, str) or not re.fullmatch(
        r'[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}', repo
    ) or repo.split('/')[-1] in ('.', '..'):
        raise ValueError('Invalid update-source.json')
    return repo


if __name__ == '__main__':
    try:
        print(read(sys.argv[1]))
    except (ValueError, KeyError, IndexError, OSError) as error:
        sys.exit(str(error))
