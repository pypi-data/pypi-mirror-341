from django.test import TestCase
from django.test.utils import override_settings

from django_super_svgs.templatetags.base import loaded_svgs


@override_settings(DEBUG=True)
class ViewTests(TestCase):
    def test_index(self):
        response = self.client.get("/svgs/")
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get("/svgs/")
        self.assertTemplateUsed(response, "django_super_svgs/index.html")

    def test_index_default_should_be_bootstrap(self):
        response = self.client.get("/svgs/")
        self.assertEqual(response.context["active"], "bootstrap")

    def test_set_active_to_hero_outline(self):
        response = self.client.get("/svgs/?svg=hero_outline")
        self.assertEqual(response.context["active"], "hero_outline")

    def test_svgs_content(self):
        response = self.client.get("/svgs/")
        svgs = response.context["svgs"]
        self.assertIsInstance(svgs, dict)
        self.assertTrue("info_square_fill" in svgs.keys())

    def test_search_not_found_term(self):
        response = self.client.get("/svgs/?q=xxxx")
        svgs = response.context["svgs"]
        self.assertEqual(len(svgs), 0)
        self.assertInHTML("No results found", response.content.decode())

    def test_search_found_term_using_hero_outline(self):
        response = self.client.get("/svgs/?q=academic&svg=hero_outline")
        svgs = response.context["svgs"]
        self.assertEqual(len(svgs), 1)
        self.assertInHTML("academic_cap", response.content.decode())

    def test_input_hidden_svg(self):
        response = self.client.get("/svgs/")
        self.assertInHTML(
            '<input type="hidden" name="svg" value="bootstrap">',
            response.content.decode(),
        )

    def test_input_hidden_svg_for_hero_solid(self):
        response = self.client.get("/svgs/?svg=hero_solid")
        self.assertInHTML(
            '<input type="hidden" name="svg" value="hero_solid">',
            response.content.decode(),
        )

    def test_invalid_svg_type_must_return_no_results_found(self):
        response = self.client.get("/svgs/?svg=xxxx")
        svgs = response.context["svgs"]
        self.assertEqual(len(svgs), 0)
        self.assertInHTML("No results found", response.content.decode())

    def test_aside_url_without_search_term(self):
        aside_names = list(loaded_svgs.keys())
        response = self.client.get("/svgs/?q=")
        self.assertEqual(response.status_code, 200)
        with self.subTest():
            for name in aside_names:
                self.assertInHTML(
                    f'<a class="aside-item {"active" if name == "bootstrap" else ""}" href="?q=&svg={name}"><span>{" ".join(name.title().split("_"))}</span></a>',
                    response.content.decode(),
                )

    def test_aside_url_with_search_term(self):
        aside_names = list(loaded_svgs.keys())
        response = self.client.get("/svgs/?q=wallet")
        self.assertEqual(response.status_code, 200)
        with self.subTest():
            for name in aside_names:
                self.assertInHTML(
                    f'<a class="aside-item {"active" if name == "bootstrap" else ""}" href="?q=wallet&svg={name}"><span>{" ".join(name.title().split("_"))}</span></a>',
                    response.content.decode(),
                )
