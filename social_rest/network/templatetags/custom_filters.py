from django import template
from ..models import Like  # Replace 'your_app' with your actual app name

register = template.Library()

@register.filter
def has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()
