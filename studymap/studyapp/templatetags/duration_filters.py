from django import template

register = template.Library()

@register.filter
def duration_format(value):
    # Converts integer duration to formatted string
    try:
        total_seconds = int(value)
    except (ValueError, TypeError):
        return value  # Return the original value if conversion fails

    days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600)      # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
