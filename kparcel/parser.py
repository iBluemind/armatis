# -*- coding: utf-8 -*-


import urllib.request
import six
from abc import abstractmethod, ABCMeta
from contextlib import closing
from weakref import WeakValueDictionary
from bs4 import BeautifulSoup
from kparcel.constants import PARSER_REQUEST_HEADER_USER_AGENT, \
    TRACKING_RESULT_PARCEL, TRACKING_RESULT_TRACKS
from kparcel.models import Parcel, Company, Tracker


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
            TRACKING_RESULT_PARCEL: self.parcel,
            TRACKING_RESULT_TRACKS: self.tracks
        }


class ParserRequest(object):
    def __init__(self, url=None, body=None, header={}):
        # API endpoint
        self.url = url
        # The body content for HTTP request
        self.body = body
        # The header for HTTP request
        self.header = header
        # Add an user agent of Internet Explorer
        self.header['User-Agent'] = PARSER_REQUEST_HEADER_USER_AGENT


@six.add_metaclass(ABCMeta)
class Parser(object):
    def __init__(self, invoice_number):
        self.source = Source()
        self._invoice_number = invoice_number

    @property
    def invoice_number(self):
        return self._invoice_number

    @property
    def parser_request(self):
        return self._parser_request

    @parser_request.setter
    def parser_request(self, parser_request):
        """
        Provide the additional HTTP request information for browsing the API

        :param ParserRequest parser_request: The HTTP request information
        """
        if not isinstance(parser_request, ParserRequest):
            raise TypeError('The parser_request must be ParserRequest!')
        self._parser_request = parser_request

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

    def _make_request(self):
        pr = self.parser_request
        return urllib.request.Request(pr.url, pr.body, pr.header)

    def _fetch(self):
        """
        Browsing the API request and return the response
        :return: The response of the API request
        """
        request = self._make_request()
        with closing(urllib.request.urlopen(request)) as response:
            return response.read()

    @abstractmethod
    def parse(self, parser, response):
        """
        Parse the response of the API request

        :param parser: The module for parsing the response
        :param str response: The response of the API request
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
        self.parse(parser, response)
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

