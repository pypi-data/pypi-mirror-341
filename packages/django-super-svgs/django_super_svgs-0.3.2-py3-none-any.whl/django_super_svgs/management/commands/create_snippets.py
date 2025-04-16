import importlib
import json
import os
import pathlib
import re
import sys

from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create svgs snippets for neovim. If you want to save as vscode, just add --vscode parameter"
    SVG_EXTENSION = ["json", "code-snippets"]
    STD_OUTPUT = "snippets"

    def add_arguments(self, parser):
        parser.add_argument(
            "-o", "--output", type=str, help="Svg's snippets output folder"
        )
        parser.add_argument(
            "--vscode",
            default=0,
            action="store_const",
            const=1,
            help="Export snippets as vscode format",
        )
        parser.add_argument(
            "--builtins",
            default=False,
            action="store_true",
            help="Export builtins svgs into snippets files.",
        )

    def handle(self, *args, **kwargs):
        apps_finder = finders.AppDirectoriesFinder()
        svgs = list(
            map(
                lambda f: pathlib.Path(f[1].location, f[0]),
                filter(
                    lambda x: re.search("svgs/.*py$", x[0]),
                    apps_finder.list(ignore_patterns=["admin", "__pycache__"]),
                ),
            )
        )

        svg_vscode_extension = kwargs.get("vscode")
        std_output_folder = kwargs.get("output") or self.STD_OUTPUT
        svg_builtins = kwargs.get("builtins")
        os.makedirs(std_output_folder, exist_ok=True)

        if svg_builtins:
            builtin_svgs = list(
                pathlib.Path(
                    pathlib.Path(__file__).parent.parent.parent,
                    "templatetags",
                    "svgs",
                ).glob("[!_]*.py")
            )
            svgs = svgs + builtin_svgs

        for svg_file in svgs:
            snippet_text = {}
            spec = importlib.util.spec_from_file_location(
                svg_file.stem, pathlib.Path(svg_file)
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

            svg_names = [d for d in dir(module) if not d.startswith("__")]
            for svg in svg_names:
                snippet_text.update(
                    {
                        svg: {
                            "prefix": f"svg.{svg_file.stem}.{svg}",
                            "description": f"SVG {svg_file.stem} - {svg}",
                            "body": [f"{{% svg {svg_file.stem} {svg} %}}"],
                        }
                    }
                )
            output_folder = f"{std_output_folder}/{svg_file.stem}.{self.SVG_EXTENSION[svg_vscode_extension]}"
            with open(output_folder, "w") as f:
                f.write(json.dumps(snippet_text, indent=4))

            if not svg_vscode_extension:
                self.create_package_file(file_path=std_output_folder)

        self.stdout.write(self.style.SUCCESS("DONE!"))

    def create_package_file(self, file_path):
        contribs = []

        for snippet in pathlib.Path(file_path).glob("[!package]*.json"):
            contribs.append(
                {"language": "htmldjango", "path": f"./{snippet.stem}.json"}
            )

        package_info = dict(
            name="nvim-snippets",
            author="Django Super SVGs",
            engines={"vscode": "^1.11.0"},
            contributes={"snippets": contribs},
        )
        with open(pathlib.Path(file_path, "package.json"), "w") as f:
            f.write(json.dumps(package_info, indent=4))
