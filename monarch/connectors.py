# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
import cStringIO


class BaseConnector(object):
    def __init__(self, settings, cmd=None):
        self.settings = settings
        self.cmd = cmd

        print(self.settings)

    def fetcher(self):
        raise NotImplementedError

    def fetch(self):
        raise NotImplementedError


class HttpConnectorMixin(object):
    def fetcher(self, **kwargs):
        if 'URL' not in self.settings:
            raise ValueError('No URL in monarch CONNECTOR settings.')
        url = self.settings['URL']
        data = None

        values = {}
        if 'DATA' in self.settings:
            values = self.settings['DATA']
        values.update(kwargs)

        data = urllib.urlencode(values)

        method = "GET"
        if "METHOD" in self.settings:
            method = self.settings['METHOD']

        if method == "GET":
            url = "%s?%s" % (url, urllib.urlencode(values))
        else:
            data = urllib.urlencode(values)

        request = urllib2.Request(self.url, data)
        opener = urllib2.build_opener()
        f = opener.open(request)
        return f


class FileConnectorMixin(object):
    def fetcher(self):
        raise NotImplementedError('TODO: create file connector mixin.')


class JsonConnectorMixin(object):
    def fetch(self, **kwargs):
        return json.load(self.fetcher())


class ModelConnectorMixin(object):
    def fetch(self):
        raise NotImplementedError('TODO: create django model connector mixin.')


class XmlConnectorMixin(object):
    def fetch(self):
        raise NotImplementedError('TODO: create xml connector mixin.')


class MockJSONConnector(BaseConnector):
    def __init__(self, settings, cmd=None):
        pass
        #self.file = settings['']

    def fetcher(self, *args, **kwargs):
        return {'error': 'This was an error on the server side :('}


class HttpJsonConnector(JsonConnectorMixin, HttpConnectorMixin, BaseConnector):
    pass


class FakeConnector(BaseConnector):
    def fetcher(self):
        pass

    def fetch(self):
        pass

