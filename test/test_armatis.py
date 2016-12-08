# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch
from armatis import Armatis
from armatis.constants import TRACKING_RESULT_PARCEL
from armatis.constants import TRACKING_RESULT_TRACKS
from armatis.parsers.d2d import DoorToDoorParser
from armatis.parsers.hanjin import HanjinParser
from armatis.parsers.hyundai import HyundaiParser
from armatis.parsers.kg_logis import KGLogisParser
from armatis.parsers.logen import LogenParser

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

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, '경기도 성남시 분당구******')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].sender, '(주*')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].receiver, '한만*')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].note, '일반')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, '배달완료')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, '2016-10-14 16:44:35')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, '분당대리점a(C15F)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, '분당대리점a(C15F)(031-769-0516)')

    @patch.object(KGLogisParser, '_fetch')
    def test_kg_logis_parser(self, _fetch):
        def fetch():
            with open('%s/kg_logis.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('kglogis', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, '서울 동작구  사당4동')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].sender, '한만종 님')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].receiver, '한*종 님')
        self.assertEqual(result[TRACKING_RESULT_PARCEL].note, '일반테스트상품')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, '고객님의 상품이 배달완료 되었습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, '2016.10.18 18:24')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, '동작')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, '010-1234-5678')

    @patch.object(HanjinParser, '_fetch')
    def test_hanjin_parser(self, _fetch):
        def fetch():
            with open('%s/hanjin.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('hanjin', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, '서울 송파 삼전')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, '배송완료되었습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, '2016-09-23 14:29')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, '잠실2(대)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, '01012345678')

    @patch.object(HyundaiParser, '_fetch')
    def test_hyundai_parser(self, _fetch):
        def fetch():
            with open('%s/hyundai.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()

        _fetch.return_value = fetch()
        armatis = Armatis('hyundai', 123456789123)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_PARCEL].address, '김포서부(대)')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, '물품을 받으셨습니다.')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].time, '2016.10.13 --:--')

    @patch.object(LogenParser, '_fetch')
    def test_logen_parser(self, _fetch):
        def fetch():
            with open('%s/logen.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('logen', 12345678912)
        result = armatis.find()

        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].status, '배송완료')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].location, '평택')
        self.assertEqual(result[TRACKING_RESULT_TRACKS][-1].phone1, '010-1234-5678')

