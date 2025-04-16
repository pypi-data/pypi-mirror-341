from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase
from parsel import Selector


class TemplateTests(TestCase):
    def setUp(self) -> None:
        self.context = Context()
        self.template_base = (
            "{% load super_svgs %}{% svg hero_outline academic_cap %}"
        )
        self.error_msg = 'The svg tag requires a svg filename followed by svg name, \n \
    and optionally followed by a list of attributes and values like attr="value"'

    def test_default_class_is_svg_container(self):
        sel = self.get_selector(string=self.template_base)
        self.assertTrue(sel.css(".svg-container"))

    def test_change_settings_default_container_class_to_my_new_class(self):
        with self.settings(SUPER_SVGS_CONTAINER_CLASSES="my-new-class"):
            sel = self.get_selector(string=self.template_base)
            self.assertTrue(sel.css(".my-new-class"))

    def test_adding_extra_class(self):
        template = '{% load super_svgs %}{% svg hero_outline academic_cap class="my-new-class" %}'
        sel = self.get_selector(string=template)
        self.assertTrue(sel.css(".svg-container.my-new-class"))

    def test_parsing_error_missing_svg_filename(self):
        template = "{% load super_svgs %}{% svg %}"

        with self.assertRaisesMessage(TemplateSyntaxError, self.error_msg):
            self.render_template(string=template)

    def test_parsing_error_missing_svg_name(self):
        template = "{% load super_svgs %}{% svg hero_outline %}"

        with self.assertRaisesMessage(TemplateSyntaxError, self.error_msg):
            self.render_template(string=template)

    def test_set_svg_fill_to_red(self):
        template = '{% load super_svgs %}{% svg hero_solid academic_cap svg:fill="#ff0000" %}'
        sel = self.get_selector(string=template)
        self.assertEqual(sel.css("svg").attrib.get("fill"), "#ff0000")

    def test_set_svg_stroke_to_4_and_svg_fill_to_red(self):
        template = '{% load super_svgs %}{% svg hero_solid academic_cap svg:stroke="4" svg:fill="#ff0000" %}'
        sel = self.get_selector(string=template)

        attrs = (
            ("stroke", "4"),
            ("fill", "#ff0000"),
        )

        for attr, value in attrs:
            with self.subTest():
                self.assertEqual(sel.css("svg").attrib.get(attr), value)

    def test_set_path_opacity_to_0_4(self):
        template = '{% load super_svgs %}{% svg hero_solid academic_cap path:fill-opacity="0.4" %}'
        sel = self.get_selector(string=template)
        self.assertTrue(sel.css("path").attrib.get("fill-opacity"), "0.4")

    def test_custom_svg_created_at_dummy_app(self):
        template = "{% load super_svgs %}{% svg mycustomsvg python_logo %}"
        sel = self.get_selector(string=template)
        self.assertTrue(sel.css("svg"))

    def render_template(self, string, context=None):
        context = Context(context or {})
        return Template(string).render(context)

    def get_selector(self, string, context=None):
        resp = self.render_template(string=string, context=context)
        return Selector(text=resp)
