from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(format_string='%H:%M of %d %b %Y'):
   return datetime.utcnow().strftime(format_string)
