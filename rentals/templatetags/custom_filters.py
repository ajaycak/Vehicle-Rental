from django import template

register = template.Library()

@register.filter
def stars(value):
    try:
        value = int(value)  # Convert the value to an integer (if it's a valid number)
        return '★' * value + '☆' * (5 - value)  # Return filled stars and empty stars to make up 5
    except (ValueError, TypeError):
        return '☆' * 5  # If there's an error, just return 5 empty stars
