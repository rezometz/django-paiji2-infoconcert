import urllib2
import dateutil.parser
import socket

from bs4 import BeautifulSoup


class InfoConcertFetcher(object):
    url = 'http://www.infoconcert.com/ville/metz-2186/concerts.html'
    labels = {
        'Concert': 'primary',
        'Festival': 'success',
    }

    def __init__(self):
        try:
            content = urllib2.urlopen(self.url, timeout=1).read()
            self.content = BeautifulSoup(content)
        except socket.timeout:
            print "Infoconcert timeout"
            self.content = None
        except urllib2.URLError:
            print "Infoconcert no internet access?"
            self.content = None

    def get_events(self, filter_free=False):
        if self.content is not None:
            events = self.content.findAll('', {
                'itemtype': 'http://data-vocabulary.org/Event',
            })
            for event in events:
                etype = event.find('', {'itemprop': 'eventType'})['content']
                free = event.find('', {'class': 'btn_gratuit'}) != None
                cost = event.find('', {'class': 'price'})
                summary = event.find('', {'itemprop': 'summary', }).text
                summary = summary.strip().title()
                org_locality = event.find('', {'itemprop': 'locality'}).text
                org_name = event.find('', {'itemprop': 'name'}).text
                date = dateutil.parser.parse(
                    event.find('', {'itemprop': 'startDate'})['datetime']
                )

                if cost is None:
                    continue

                if not filter_free or free:
                    yield {
                        'type': etype,
                        'summary': summary,
                        'organization': {
                            'locality': org_locality,
                            'name': org_name,
                        },
                        'date': date,
                        'url': 'http://www.infoconcert.com/',
                        'label': self.labels.get(etype, 'danger'),
                        'is_free': free,
                        'cost': cost.get_text().strip(),
                    }
