from django.templatetags.static import static
from django.urls import reverse
from sesame.utils import get_query_string

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "get_query_string": get_query_string,
        }
    )
    return env
