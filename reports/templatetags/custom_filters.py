from django import template

register = template.Library()

@register.filter
def double_length(value):
	return len(value) * 2