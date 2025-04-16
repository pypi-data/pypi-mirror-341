from django.core.cache import cache
from django.views.generic import TemplateView

from .templatetags.base import all_svgs, loaded_svgs


class Index(TemplateView):
    template_name = "django_super_svgs/index.html"
    svg_default = "bootstrap"
    version = "0.3.0"
    cache_name = "svgs_list"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.svgs = self.get_all_svgs()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_term = self.request.GET.get("q", "")
        svg_name = self.request.GET.get("svg", self.svg_default)
        svg_names = list(loaded_svgs.keys())
        svg_names.sort()

        context["active"] = svg_name
        context["version"] = self.version
        context["svgs"] = self.get_svgs(svg_name, search_term)
        context["svg_names"] = svg_names

        return context

    def get_svgs(self, name, tag):
        if name not in self.svgs.keys():
            return {}

        return dict(
            (k, v)
            for k, v in self.svgs.get(name).items()
            if k.__contains__(tag)
        )

    def get_all_svgs(self):
        if not cache.get(self.cache_name):
            cache.set(self.cache_name, all_svgs(loaded_svgs))

        return cache.get(self.cache_name)
