from urllib.parse import quote_plus
from datetime import datetime, date
import dateutil.parser
import requests


class atlas_request_error(Exception):
    pass


class atlas_server_error(Exception):
    pass


class atlas_request:
    ATLAS_API_KEY = None
    ATLAS_API_BASE_URL = 'https://atlas.infegy.com/api/v2/'

    def __init__(self, query, **kwargs):
        self.query = query

        # Parse args
        for k, v in kwargs.items():
            if isinstance(k, str):
                k = k.strip()
            if isinstance(v, str):
                v = v.strip()
            if k and v:
                setattr(self, k, v)

        self.__request_cache = {}

    def __type_massage__(self, t):
        if isinstance(t, bool):
            return '1' if t else '0'
        if isinstance(t, list) or isinstance(t, tuple):
            return ','.join(str(v) for v in t)
        if isinstance(t, datetime):
            return t.date().isoformat()
        if isinstance(t, date):
            return t.isoformat()
        else:
            return str(t)

    def uri(self, endpoint):
        if self.ATLAS_API_KEY is None:
            raise atlas_request_error(
                "You must set an Atlas API key on this class before use, e.g.:"
                "from atlas_api import atlas_request\n"
                "atlas_request.ATLAS_API_KEY='YOUR_KEY_HERE'")

        uri_string = self.ATLAS_API_BASE_URL + \
            endpoint + '?api_key=' + self.ATLAS_API_KEY

        for k in [k for k in dir(self) if not callable(getattr(self, k))
                  and not k.startswith('_') and not k.isupper()]:
            v = getattr(self, k)
            if v is None:
                continue

            uri_string += '&%s=%s' % (k, quote_plus(self.__type_massage__(v)))
        return uri_string

    def url(self, endpoint):
        return self.uri(endpoint)

    def run_raw(self, endpoint, skip_cache=False):
        if not skip_cache and endpoint in self.__request_cache:
            return self.__request_cache[endpoint]

        r = requests.get(self.uri(endpoint))
        if r.status_code >= 400 and r.status_code < 500:
            raise atlas_request_error('Your request has an error (code %d): %s'
                                      % (r.status_code, r.json()['status_message']))
        elif r.status_code >= 500:
            if r.text.startswith('{'):
                raise atlas_server_error('Atlas has errored (code %d): %s'
                                         % (r.status_code, r.json()['status_message']))
            else:
                raise atlas_server_error(
                    'Atlas error (code %d): %s' % (r.status_code, r.text))

        try:
            raw_json = r.json()
        except BaseException:
            raise atlas_server_error(
                'Atlas returned something that can\'t be parsed as JSON')
        if not isinstance(raw_json, object):
            raise atlas_server_error(
                'Atlas returned something that isn\'t a JSON object')

        if 'status' not in raw_json:
            raise atlas_server_error('Atlas returned an object with no status')
        if raw_json['status'] != 'OK':
            raise atlas_server_error('Atlas a bad status with no error code. '
                                     'Status: %s, Status message: %s',
                                     raw_json['status'], raw_json.get('status_message', ''))

        self.__request_cache[endpoint] = raw_json

        return raw_json

    def run(self, endpoint, skip_cache=False):
        raw_json = self.run_raw(endpoint, skip_cache)
        return atlas_response(raw_json)

    # The various endpoint utility functions...

    def volume(self):
        return self.run('volume').output

    def posts(self):
        return self.run('posts').output

    def topics(self):
        return self.run('topics').output

    def positive_topics(self):
        return self.run('positive-topics').output

    def negative_topics(self):
        return self.run('negative-topics').output

    def brands(self):
        return self.run('brands').output

    def hashtags(self):
        return self.run('hashtags').output

    def topic_clusters(self):
        return self.run('topic-clusters').output

    def headlines(self):
        return self.run('headlines').output

    def sentiment(self):
        return self.run('sentiment').output

    def positive_keywords(self):
        return self.run('positive-keywords').output

    def negative_keywords(self):
        return self.run('negative-keywords').output

    def linguistics_stats(self):
        return self.run('linguistics-stats').output

    def themes(self):
        return self.run('themes').output

    def emotions(self):
        return self.run('emotions').output

    def languages(self):
        return self.run('languages').output

    def timeofday(self):
        return self.run('timeofday').output

    def channels(self):
        return self.run('channels').output

    def gender(self):
        return self.run('gender').output

    def states(self):
        return self.run('states').output

    def countries(self):
        return self.run('countries').output

    def home_ownership(self):
        return self.run('home-ownership').output

    def income(self):
        return self.run('income').output

    def household_value(self):
        return self.run('household-value').output

    def education(self):
        return self.run('education').output

    def demographics(self):
        return self.run('demographics').output

    def ages(self):
        return self.run('ages').output

    def influence_distribution(self):
        return self.run(
            'influence-distribution').output

    def influencers(self):
        return self.run('influencers').output

    def interests(self):
        return self.run('interests').output

    def post_interests(self):
        return self.run('post-interests').output

    def query_test(self):
        return self.run('query-test').output

    def events(self):
        return self.run('events').output

    def stories(self):
        return self.run('stories').output

    def entities(self):
        return self.run('entities').output

    def meta(self):
        return self.run('volume').query_meta


class atlas_response(object):
    def __init__(self, obj):
        for k, v in obj.items():
            if isinstance(v, str):
                if 8 < len(v) < 22:
                    try:
                        dt = dateutil.parser.parse(v)
                        setattr(self, k, dt)
                        continue
                    except (ValueError, OverflowError):
                        pass
                setattr(self, k, v)
            elif type(v) in (float, int, date, datetime, bool):
                setattr(self, k, v)
            elif isinstance(v, dict):
                setattr(self, k, atlas_response(v))
            else:
                setattr(self, k, [])
                for o in v:
                    if isinstance(o, dict):
                        getattr(self, k).append(atlas_response(o))
                    else:
                        getattr(self, k).append(o)
