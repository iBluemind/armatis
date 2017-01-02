# -*- coding: utf-8 -*-


from time import sleep
import six
from abc import abstractmethod, ABCMeta
from weakref import WeakValueDictionary
from bs4 import BeautifulSoup
import requests
from requests import Request
from armatis.models import Parcel, Company, Tracker


def dict2parser_request(pr_dict):
    pr = ParserRequest(
        url=pr_dict.get('url'),
        method=pr_dict.get('method'),
        body=pr_dict.get('body'),
        header=pr_dict.get('header')
    )
    return pr


class Source(object):
    def __init__(self):
        self.tracker = Tracker()

    @property
    def tracks(self):
        return self.tracker.tracks

    @property
    def parcel(self):
        return self._parcel

    @parcel.setter
    def parcel(self, parcel):
        if not isinstance(parcel, Parcel):
            raise TypeError('The parcel must be Parcel!')
        self._parcel = parcel

    def add_track(self, new_track):
        self.tracker.add_track(new_track)

    def summary(self):
        return {
            'parcel': self.parcel,
            'tracks': self.tracks
        }


class ParserRequest(object):
    def __init__(self, url=None, method=None, body=None, header=None):
        # API endpoint
        if url is None:
            raise ValueError('The URL must be set!')
        self.url = url
        # HTTP request method
        self.method = method if method is not None else 'GET'
        # The body content for HTTP request
        self.body = body
        # The header for HTTP request
        if header is None:
            header = {}
        self.header = header


class RequestManager(object):
    """
    Provide the additional HTTP request information for browsing the API

    """
    def __init__(self, user_agent):
        self.requests = []
        self._current = 0
        self.user_agent = user_agent

    def add_request(self, new_request):
        if not isinstance(new_request, ParserRequest):
            raise TypeError('The new_request must be ParserRequest!')
        self.requests.append(new_request)

    def _make_request(self, request):
        headers = request.header
        headers['User-Agent'] = self.user_agent
        return Request(request.method, request.url, data=request.body, headers=headers)

    def __iter__(self):
        for request in self.requests:
            yield self._make_request(request)

    def __len__(self):
        return len(self.requests)


@six.add_metaclass(ABCMeta)
class Parser(object):
    def __init__(self, invoice_number, config):
        self.source = Source()
        self.config = config
        self._invoice_number = invoice_number
        self.request_manager = RequestManager(config['USER_AGENT_STRING'])

    @property
    def invoice_number(self):
        return self._invoice_number

    @property
    def parcel(self):
        return self.source.parcel

    @parcel.setter
    def parcel(self, parcel):
        """
        Store the information of the found parcel

        :param Parcel parcel: The information of the parcel
        """
        if not isinstance(parcel, Parcel):
            raise TypeError('The parcel must be Parcel!')
        self.source.parcel = parcel

    @property
    def requests(self):
        return self.request_manager

    @requests.setter
    def requests(self, requests):
        for request in requests:
            if isinstance(request, ParserRequest):
                self.request_manager.add_request(request)
            elif isinstance(request, dict):
                self.request_manager.add_request(dict2parser_request(request))
            else:
                raise TypeError('The member of requests must be dict or ParserRequest!')

    def add_request(self, new_request):
        return self.request_manager.add_request(new_request)

    def _fetch(self):
        """
        Browsing the API request and return the response
        :return: The response of the API request
        """
        with requests.Session() as session:
            for index, request in enumerate(self.request_manager):
                if index != 0:
                    sleep(self.config['MULTIPLE_REQUEST_PERIOD'])
                prepared = session.prepare_request(request)
                response = session.send(prepared)
                if index == (len(self.request_manager) - 1):
                    if self.config.get('RESPONSE_ENCODING', None):
                        response.encoding = self.config['RESPONSE_ENCODING']
                    return response.text

    @abstractmethod
    def parse(self, parser):
        """
        Parse the response of the API request

        :param parser: The module for parsing the response
        """
        raise NotImplemented("Please implement the method 'parse'!")

    def parser(self, doc):
        """
        The module for parsing the response of the API request

        :param str doc: The response of the API request
        :return: The module for parsing the response
        """
        return BeautifulSoup(doc, 'lxml')

    def add_track(self, new_track):
        """
        Add the tracking status information

        :param Track new_track: The tracking status information
        """
        self.source.add_track(new_track)

    def result(self):
        """
        Get the found parcel tracking informations

        :return: The found parcel and tracking informations
        :rtype: dict
        """
        return self.source.summary()

    def find(self):
        response = self._fetch()
        parser = self.parser(response)
        self.parse(parser)
        return self.result()


class ParserManager(object):
    def __init__(self):
        self._companies = {}
        self._parsers = WeakValueDictionary()

    def register_parser(self, company, new_parser):
        """
        Register the new parser

        :param Company company: The new company
        :param Parser new_parser: The new parser
        """
        if not isinstance(company, Company):
            raise TypeError('The company must be Company!')
        if not issubclass(new_parser, Parser):
            raise TypeError('The new_parser must be Parser!')
        self._companies[company.code] = company
        self._parsers[company.code] = new_parser

    def __getitem__(self, company_code):
        return self._companies[company_code], self._parsers[company_code]

    def __iter__(self):
        """
        Registered parsers and companies

        :return: The list of company object and parser object
        :rtype: dict
        """
        for k, v in self._parsers.items():
            yield (self._companies[k], v)

    def __len__(self):
        return len(self._parsers)
