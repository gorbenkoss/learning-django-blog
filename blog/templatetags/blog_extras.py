from django import template
import datetime

register = template.Library()

@register.filter(name='format_post_date')
def format_post_date(value):
    """
    Custom template filter to format the date of a post based on how recently it was posted.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - value

    if diff < datetime.timedelta(minutes=1):
        return "just now"
    elif diff < datetime.timedelta(hours=1):
        return f"{int(diff.seconds / 60)} minutes ago"
    elif diff < datetime.timedelta(days=1):
        return f"today, at {value.strftime('%I:%M %p').lstrip('0')}"
    else:
        return value.strftime("%B %d, %Y, %I:%M %p")