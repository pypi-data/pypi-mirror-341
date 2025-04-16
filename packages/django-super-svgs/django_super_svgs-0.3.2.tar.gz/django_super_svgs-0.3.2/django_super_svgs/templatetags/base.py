import functools
import importlib
import re
import sys
from pathlib import Path

from django import template
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

KWARGS_RE = _lazy_re_compile(r"(\w+:)?([a-zA-Z-_]+)=(.+)")

SVG_CONTAINER_CLASS = "svg-container"

ERROR_MSG = _(
    'The svg tag requires a svg filename followed by svg name, \n \
    and optionally followed by a list of attributes and values like attr="value"'
)

DEFAULT_SVGS = [
    "bootstrap",
    "dripicons",
    "hero_outline",
    "hero_solid",
    "material",
]


class RenderSvg(template.Node):
    """Return a choosen svg rendered."""

    extra_classes = ""
    svg_tags = []
    path_tags = []

    def __init__(self, parser, token):
        self.parser = parser
        self.token = token
        self.tag_name, *self.bits = token.split_contents()
        self.args, self.kwargs, self.dot_kwargs = self.token_kwargs(
            self.bits, self.parser
        )

        if len(self.args) < 2:
            raise template.TemplateSyntaxError(ERROR_MSG)

        self.svg_file = self.args[0]
        self.svg_name = self.args[1]

        if "svg" in self.dot_kwargs.keys():
            self.svg_tags = self.dot_kwargs.get("svg")

        if "path" in self.dot_kwargs.keys():
            self.path_tags = self.dot_kwargs.get("path")

    def _parse_kwargs(self):
        tags = []
        for k, v in self.kwargs.items():
            value = v.var
            if v.var.startswith("{{"):
                var_from_token = re.sub(r"[}{\s]", "", v.var)
                value = template.Variable(var_from_token).resolve(
                    context=self.context
                )

            if k == "class":
                self.extra_classes = value
                continue

            tags.append(f'{k}="{value}"')

        return " ".join(tags)

    def _parse_dot_kwargs(self, html, tag_name, tags):
        for tag in tags:
            for k, v in tag.items():
                pattern = rf"{k}=\"[#A-Za-z0-9]+\""
                sub = re.findall(rf"<{tag_name}.*>", html)[0]
                new_sub = re.findall(pattern, sub)
                if not new_sub:
                    ns = re.sub(
                        rf"<{tag_name}\s", f'<{tag_name} {k}="{v.var}"', sub
                    )
                    html = html.replace(sub, ns)
                for n in new_sub:
                    html = html.replace(n, f'{k}="{v.var}"')

        return html

    def token_kwargs(self, bits, parser):
        kwargs = {}
        dot_kwargs = {}
        args = []

        for bit in bits:
            match = KWARGS_RE.match(bit)
            if not match:
                args.append(bit)
                continue

            mg = match.groups()
            if mg:
                if mg[0] is None:
                    kwargs[mg[1]] = parser.compile_filter(mg[2])
                    continue

                key = mg[0].strip(":")
                value = {mg[1]: parser.compile_filter(mg[2])}
                if key in dot_kwargs.keys():
                    dot_kwargs.get(key).append(value)
                else:
                    dot_kwargs[key] = [value]

        return args, kwargs, dot_kwargs

    def render(self, context):
        self.context = context
        self.tags = self._parse_kwargs()

        self.svg_file = context.get("svg_file", self.svg_file)
        self.svg_name = context.get("svg_name", self.svg_name)

        module = loaded_svgs.get(self.svg_file, self.svg_file)
        html = base_html(
            module.get(self.svg_name),
            self.extra_classes,
            self.tags,
        )
        html = self._parse_dot_kwargs(html, "svg", self.svg_tags)
        html = self._parse_dot_kwargs(html, "path", self.path_tags)

        return mark_safe(html)


def base_html(body, extra_class="", tags=""):
    class_name = getattr(
        settings, "SUPER_SVGS_CONTAINER_CLASSES", SVG_CONTAINER_CLASS
    )
    html = f"""
        <div class="{class_name} {extra_class}" {tags}>
            {body}
        </div>
    """
    return html


def svgs_from_file(file_name):
    return list(
        filter(
            lambda x: not x.startswith("__"),
            dir(sys.modules.get(file_name)),
        )
    )


def svg_body(module, attribute):
    return getattr(sys.modules.get(module), attribute, "")


@functools.cache
def load_svgs():
    """Return a dict with all svgs (only svg body)."""
    app_configs = apps.get_app_configs()
    svgs_dict = dict()
    apps_ = list(
        map(
            lambda y: (y.name, y),
            filter(
                lambda x: not x.name.__contains__("django"),
                app_configs,
            ),
        )
    )

    for app in apps_:
        app_storage = FileSystemStorage(Path(app[1].path, "templatetags"))
        if app_storage.exists("svgs"):
            _, files = app_storage.listdir("svgs")
            for file in files:
                importlib.import_module(
                    f"{app[0]}.templatetags.svgs.{Path(file).stem}"
                )
                svgs_dict[Path(file).stem] = svg_content_from_file(
                    f"{app[0]}.templatetags.svgs.{Path(file).stem}"
                )

    for item in DEFAULT_SVGS:
        importlib.import_module(f"django_super_svgs.templatetags.svgs.{item}")
        svgs_dict[item] = svg_content_from_file(
            f"django_super_svgs.templatetags.svgs.{item}"
        )

    return svgs_dict


def svg_content_from_file(file_name):
    tags = svgs_from_file(file_name)
    sv = dict()
    for tag in tags:
        sv[tag] = mark_safe(svg_body(file_name, tag))

    return sv


def all_svgs(loaded_svgs):
    """Return all loaded svgs."""
    bkp = dict()
    for k, v in loaded_svgs.items():
        bkp[k] = dict((k, mark_safe(base_html(v))) for k, v in v.items())

    return bkp


loaded_svgs = load_svgs()
