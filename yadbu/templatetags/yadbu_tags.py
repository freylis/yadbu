from django import template

from .. import api_client


register = template.Library()


@register.inclusion_tag('admin/yadbu/statistic_block.html')
def statistic_block():
    total_statistic = api_client.get_disk_info()
    print(total_statistic.json())
    return {
        'foo': total_statistic,
    }