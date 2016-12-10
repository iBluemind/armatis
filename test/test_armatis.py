# -*- coding: utf-8 -*-

try:
    # for >= python 3.3
    from unittest.mock import patch
except:
    from mock import patch
import os
import unittest
from armatis import Armatis
from armatis.constants import TRACKING_RESULT_PARCEL
from armatis.constants import TRACKING_RESULT_TRACKS
from armatis.parsers.d2d import DoorToDoorParser
from armatis.parsers.hanjin import HanjinParser
from armatis.parsers.hyundai import HyundaiParser
from armatis.parsers.kg_logis import KGLogisParser
from armatis.parsers.logen import LogenParser

# for python3
if str is not bytes:
    unicode = str

DIR_MOCK_RESPONSES = '%s/mock_responses' % os.path.dirname(os.path.realpath(__file__))


class ArmatisTest(unittest.TestCase):
    def test_supported_companies(self):
        armatis = Armatis()
        supported_companies = armatis.supported_companies()
        compared_list = [{'name': 'CJ대한통운', 'code': 'cj'},
                         {'name': 'CVSNet편의점택배', 'code': 'cvs'},
                         {'name': 'EMS', 'code': 'ems'},
                         {'name': '우체국택배', 'code': 'epost'},
                         {'name': '한진택배', 'code': 'hanjin'},
                         {'name': '합동택배', 'code': 'hapdong'},
                         {'name': '현대택배', 'code': 'hyundai'},
                         {'name': 'KGB택배', 'code': 'kgb'},
                         {'name': '로젠택배', 'code': 'logen'},
                         {'name': 'GTX로지스', 'code': 'gtx'},
                         {'name': 'KG로지스', 'code': 'kglogis'}]

        for company in compared_list:
            self.assertIn(company, supported_companies)

    @patch.object(DoorToDoorParser, '_fetch')
    def test_cj_parser(self, _fetch):
        def fetch():
            with open('%s/d2d.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('cj', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, u'경기도 성남시 분당구******')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].sender, u'(주*')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].receiver, u'한만*')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].note, u'일반')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, u'배달완료')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, u'2016-10-14 16:44:35')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, u'분당대리점a(C15F)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, u'분당대리점a(C15F)(031-769-0516)')

    @patch.object(KGLogisParser, '_fetch')
    def test_kg_logis_parser(self, _fetch):
        def fetch():
            with open('%s/kg_logis.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('kglogis', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, u'서울 동작구  사당4동')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].sender, u'한만종 님')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].receiver, u'한*종 님')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].note, u'일반테스트상품')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, u'고객님의 상품이 배달완료 되었습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, u'2016.10.18 18:24')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, u'동작')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, u'010-1234-5678')

    @patch.object(HanjinParser, '_fetch')
    def test_hanjin_parser(self, _fetch):
        def fetch():
            with open('%s/hanjin.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('hanjin', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, u'서울 송파 삼전')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, u'배송완료되었습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, u'2016-09-23 14:29')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, u'잠실2(대)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, u'01012345678')

    @patch.object(HyundaiParser, '_fetch')
    def test_hyundai_parser(self, _fetch):
        def fetch():
            with open('%s/hyundai.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('hyundai', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, u'김포서부(대)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, u'물품을 받으셨습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, u'2016.10.13 --:--')

    @patch.object(LogenParser, '_fetch')
    def test_logen_parser(self, _fetch):
        def fetch():
            with open('%s/logen.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('logen', 12345678912)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, u'배송완료')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, u'평택')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, u'010-1234-5678')
