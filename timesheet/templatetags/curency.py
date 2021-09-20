from django import template
register = template.Library()


@register.simple_tag
def comma_rial(obj):
    return "{:,.0f} ریال".format(float(obj))

@register.simple_tag
def get_jdatetime(datetime):
    return str(datetime)


@register.simple_tag
def remove_second(obj):
    return ":".join(str(obj).split(":")[0:2])