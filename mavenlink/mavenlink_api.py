# -*- coding: UTF-8 -*-
import re
import json
import requests
import urlparse

import logging
logger = logging.getLogger(__name__)


class BadApiServesHTMLInsteadOfJsonExcepton(Exception):
    message = 'This api, is misconfigured. It serves HTML instead of a valid api format (json) as a response'


class InvalidApiResponse(Exception): pass


class Session:
    """
    Session object
    """
    site = 'https://api.mavenlink.com/api/v1/'
    token = None

    def __init__(self, token, **kwargs):
        self.token = token


class BaseApi:
    r = requests
    http_methods_allowed = ['get', 'post', 'patch', 'put', 'delete']

    def __init__(self, session, **kwargs):
        self.session = session
        self.token = session.token
        self.response = self.response_json = {}
        self.params = kwargs

    @property
    def base_url(self):
        return self.session.site

    @property
    def status_code(self):
        return getattr(self.response, 'status_code', None)

    @property
    def ok(self):
        return getattr(self.response, 'ok', None)

    @property
    def parse_uri(self):
        uri = self.uri

        for k, v in self.params.iteritems():
            key = ':{key}'.format(key=k)
            uri = uri.replace(key, str(v))

        return re.sub(r'\/\:(\w)+', '', uri)

    def headers(self, **kwargs):
        # We ONLY talk json, XML is very 1995 ;)
        headers = {
            'Content-Type': 'application/json; charset=utf-8;',
            'Accept': 'application/json;'
        }
        headers.update(kwargs)
        return headers

    def wrap_namespace(self, **kwargs):
        """
        Wrap all posted data in the structure that Mavenlink expects
        A flat dict with all the attributes just kinda mixed in there
        """
        kwargs.update({
            'apikey': self.token,
            'demo': self.session.is_demo.real  # Convert bool to 0 or 1 for php api
        })
        return json.dumps({'data': kwargs})

    def endpoint(self, *args, **kwargs):
        return urlparse.urljoin(self.base_url, self.parse_uri, *args, **kwargs)

    def process(self, response):
        self.response = response

        if response.ok is True:

            try:
                self.response_json = self.response.json()
                return self.response_json

            except ValueError as e:
                if e.message == 'No JSON object could be decoded':
                    raise BadApiServesHTMLInsteadOfJsonExcepton(e.message)
                else:
                    raise InvalidApiResponse(e.message)

        #
        # Handle the bad CLI api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        raise InvalidApiResponse('Mavenlink Api returned (%s) an invalid response: %s %s' % (response.status_code, response.url, response.content))

    def get(self, **kwargs):
        if 'get' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.get(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))

    def post(self, **kwargs):
        if 'post' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.post(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def put(self, **kwargs):
        if 'put' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.put(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def patch(self, **kwargs):
        if 'patch' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.patch(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def delete(self, **kwargs):
        if 'delete' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.delete(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))


class Timesheets(BaseApi):
    uri = 'timesheet_submissions'
    http_methods_allowed = ['post', 'get']


class Payment(BaseApi):
    uri = 'payment/init'

    def to_cents(self, amount):
        amount = str(amount).split('.')

        dollar = int(amount[0])

        try:
            cents = int(amount[1])
        except:
            cents = 0

        return (dollar * 100) + cents

    def make_payment(self, amount, payment_type, url_success, url_failure, url_push, **kwargs):
        """
        Make a request for payment,
        expect to get a data object back that contains an iframe that the user
        can confirm their payment with
        """
        self.send_data = {
            'amount': self.to_cents(amount=amount),
            'payment_type': payment_type,
            'url_success': url_success,
            'url_failure': url_failure,
            'url_push': url_push,
            'labels': self.session.labels,
        }
        self.send_data.update(kwargs)

        return self.post(**self.send_data)

    class Status(BaseApi):
        uri = 'payment/status'

    def status(self, hash):
        return self.Status(session=self.session).post(hash=hash)

    class CapturePreAuthorizedPayment(BaseApi):
        uri = 'payment/:hash/capture'

    def capture_preauthorized_payment(self, token):
        service = self.CapturePreAuthorizedPayment(session=self.session,
                                                   hash=token)
        return service.post()

    class CancelPreAuthorizedPayment(BaseApi):
        uri = 'payment/:hash/cancel'

    def cancel_preauthorized_payment(self, token):
        service = self.CancelPreAuthorizedPayment(session=self.session,
                                                  hash=token)
        return service.post()