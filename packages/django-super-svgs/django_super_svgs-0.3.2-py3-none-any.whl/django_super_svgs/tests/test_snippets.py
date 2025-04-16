import json
import pathlib
import shutil
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class SnippetsTests(TestCase):
    def setUp(self) -> None:
        self.package_json = {
            "name": "nvim-snippets",
            "author": "Django Super SVGs",
            "engines": {"vscode": "^1.11.0"},
            "contributes": {
                "snippets": [
                    {"language": "htmldjango", "path": "./mycustomsvg.json"}
                ]
            },
        }
        self.mycustomsvg = {
            "python_logo": {
                "prefix": "svg.mycustomsvg.python_logo",
                "description": "SVG mycustomsvg - python_logo",
                "body": ["{% svg mycustomsvg python_logo %}"],
            }
        }

    def tearDown(self):
        snippets = pathlib.Path("snippets")
        snipp = pathlib.Path("snipp")

        if snippets.exists():
            shutil.rmtree("snippets")

        if snipp.exists():
            shutil.rmtree("snipp")

    def test_command_create_snippets(self):
        out = StringIO()
        call_command("create_snippets", stdout=out)

        path = pathlib.Path("snippets")

        files = [
            path / "mycustomsvg.json",
            path / "package.json",
        ]

        files_list = sorted(list(path.glob("*.json")))

        self.assertIn("DONE!", out.getvalue())
        self.assertListEqual(files_list, files)

        with open(path / "package.json", "rb") as f:
            json_file = json.load(f)
            self.assertEqual(json_file, self.package_json)

        with open(path / "mycustomsvg.json", "rb") as f:
            json_file = json.load(f)
            self.assertEqual(json_file, self.mycustomsvg)

    def test_command_create_snippets_from_custom_folder(self):
        out = StringIO()
        path = pathlib.Path("snipp")
        call_command("create_snippets", output="snipp", stdout=out)

        files = [
            path / "mycustomsvg.json",
            path / "package.json",
        ]

        files_list = sorted(list(path.glob("*.json")))

        self.assertIn("DONE!", out.getvalue())
        self.assertListEqual(files_list, files)

    def test_command_create_builtins_snippets(self):
        out = StringIO()
        path = pathlib.Path("snipp")
        call_command(
            "create_snippets", builtins=True, output="snipp", stdout=out
        )

        files = [
            path / "bootstrap.json",
            path / "dripicons.json",
            path / "hero_outline.json",
            path / "hero_solid.json",
            path / "material.json",
            path / "mycustomsvg.json",
            path / "package.json",
        ]

        files_list = sorted(list(path.glob("*.json")))

        self.assertIn("DONE!", out.getvalue())
        self.assertListEqual(files_list, files)

    def test_command_create_snippets_for_vscode(self):
        out = StringIO()
        path = pathlib.Path("snipp")
        call_command(
            "create_snippets", vscode=True, output="snipp", stdout=out
        )

        files = [
            path / "mycustomsvg.code-snippets",
        ]

        files_list = sorted(list(path.glob("*.code-snippets")))

        self.assertIn("DONE!", out.getvalue())
        self.assertListEqual(files_list, files)
