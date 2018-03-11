from django import template


register = template.Library()


@register.filter
def to_laptime(total_millis):
    seconds_left, millis = divmod(total_millis, 1000)
    minutes_left, seconds = divmod(seconds_left, 60)
    hours, minutes = divmod(minutes_left, 3600)
    parts = []
    if hours:
        parts.append('{:01}'.format(hours))
    if minutes:
        parts.append('{:02}'.format(minutes))
    parts.append('{:06.3f}'.format(seconds + (millis/1000)))

    return ":".join(parts)
