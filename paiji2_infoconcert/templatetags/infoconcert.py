import itertools

from django import template

from paiji2_infoconcert.fetcher import InfoConcertFetcher


register = template.Library()


@register.inclusion_tag('infoconcert/block.html')
def next_concerts(nb=5, filter_free=False):
    events = InfoConcertFetcher().get_events(filter_free=filter_free)
    return {
        'events': itertools.islice(events, 0, nb),
    }
