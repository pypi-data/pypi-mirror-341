# Django Super SVGs

Django super svgs is a tool for render svg templates using Django templatetags.

## Installation

via pip:

```shell
pip install django-super-svgs
```

or poetry:

```shell
poetry add django-super-svgs
```

## Configuration

Add `django_super_svgs` after django apps in `INSTALLED_APPS` on `settings.py`:

```
INSTALLED_APPS = (
    ...
    'django_super_svgs',
)
```

## Usage

By default `django-super-svgs` provides these svgs:

- [bootstrap](https://icons.getbootstrap.com/)
- [dripicons](http://demo.amitjakhu.com/dripicons/)
- [heroicons](https://heroicons.com/)
- [material icons](https://github.com/material-icons/material-icons/)


Load the tag `super_svgs` in your html file, then use `svg` followed by `svg type` [ bootstrap, dripicons, hero_outline, hero_solid ] and `svg name`:

```htmldjango
{% load super_svgs %}

{% svg hero_outline check_circle %}
```

## Documentation

You can find the documentation [here](https://lucasf_dev.gitlab.io/django-super-svgs/)
