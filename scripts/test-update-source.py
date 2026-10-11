#!/usr/bin/env python3
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('update_source', Path(__file__).with_name('read-update-source.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UpdateSourceTests(unittest.TestCase):
    def test_build_input_rejects_urls_paths_and_linker_injection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'source.json'
            for repository in ['', 'o/..', 'o/.', 'o/r/extra', 'https://github.com/o/r', 'o/r -X main.version=bad', 'o/r?x=y', '-o/r', None]:
                path.write_text(json.dumps(dict(schema=1, repository=repository)))
                with self.assertRaises(ValueError): module.read(path)
            for repository in ['chenpingonline/Clash-for-fnos', 'chenpingonline/Clash-for-fnos-update-test']:
                path.write_text(json.dumps(dict(schema=1, repository=repository)))
                self.assertEqual(module.read(path), repository)
            path.write_text(json.dumps(dict(schema=2, repository='owner/repo')))
            with self.assertRaises(ValueError): module.read(path)


if __name__ == '__main__': unittest.main()
