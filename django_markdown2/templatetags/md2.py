"""
Markdown2 filter, requires the python-markdown2 library from
http://code.google.com/p/python-markdown2

This code is based on django's markup contrib.
"""

from django import template
from django.conf import settings
import sys

if sys.version_info.major == 2:
    from django.utils.encoding import force_unicode
else:
    force_unicode = lambda text: text


from django.utils.safestring import mark_safe

register = template.Library()

def markdown(value, arg=''):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown supports.

    Syntax::

        {{ value|markdown2:"extension1_name,extension2_name..." }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    """
    try:
        import markdown2
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in {% markdown %} filter: The python-markdown2 library isn't installed.")
        return force_unicode(value)
    else:
        def parse_extra(extra):
            if ':' not in extra:
                return (extra, {})
            name, values = extra.split(':', 1)
            values = dict((str(val.strip()), True) for val in values.split('|'))
            return (name.strip(), values)

        extras = (e.strip() for e in arg.split(','))
        extras = dict(parse_extra(e) for e in extras if e)

        if 'safe' in extras:
            del extras['safe']
            safe_mode = True
        else:
            safe_mode = False

        return mark_safe(markdown2.markdown(force_unicode(value), extras=extras, safe_mode=safe_mode))
markdown.is_safe = True

register.filter(markdown)
