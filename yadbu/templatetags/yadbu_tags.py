from django import template

from .. import api_client


register = template.Library()


@register.inclusion_tag('admin/yadbu/statistic_block.html')
def statistic_block():
    return api_client.get_disk_info()
