from django import template
register = template.Library()

# https://stackoverflow.com/questions/5352455/obtain-the-first-part-of-an-url-from-django-template
@register.tag
def variables(request):
        url_parts = request.path.split('/')
        return {
            'url_part_1': url_parts[1],
        }