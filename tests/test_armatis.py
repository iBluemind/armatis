# -*- coding: utf-8 -*-
from armatis.parsers.epost import EPostParser
from armatis.parsers.hapdong import HapdongParser

try:
    # for >= python 3.3
    from unittest.mock import patch
except:
    from mock import patch
import os
import unittest
from io import open
from armatis import Armatis
from armatis.parsers.d2d import DoorToDoorParser
from armatis.parsers.hanjin import HanjinParser
from armatis.parsers.lotte import LotteParser
from armatis.parsers.kg_logis import KGLogisParser
from armatis.parsers.logen import LogenParser, GTXParser
from armatis.parsers.ems import EMSParser
from armatis.parsers.kgb import KGBParser

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
                         {'name': '롯데택배', 'code': 'lotte'},
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

        self.assertEqual(result['parcel'].address, u'경기도 성남시 분당구******')
        self.assertEqual(result['parcel'].sender, u'(주*')
        self.assertEqual(result['parcel'].receiver, u'한만*')
        self.assertEqual(result['parcel'].note, u'일반')
        self.assertEqual(result['tracks'][-1].status, u'배달완료')
        self.assertEqual(result['tracks'][-1].time, u'2016-10-14 16:44:35')
        self.assertEqual(result['tracks'][-1].location, u'분당대리점a(C15F)')
        self.assertEqual(result['tracks'][-1].phone1, u'분당대리점a(C15F)(031-769-0516)')

    @patch.object(KGLogisParser, '_fetch')
    def test_kg_logis_parser(self, _fetch):
        def fetch():
            with open('%s/kg_logis.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('kglogis', 123456789123)
        result = armatis.find()

        self.assertEqual(result['parcel'].address, u'서울 동작구  사당4동')
        self.assertEqual(result['parcel'].sender, u'한만종 님')
        self.assertEqual(result['parcel'].receiver, u'한*종 님')
        self.assertEqual(result['parcel'].note, u'일반테스트상품')
        self.assertEqual(result['tracks'][-1].status, u'고객님의 상품이 배달완료 되었습니다.')
        self.assertEqual(result['tracks'][-1].time, u'2016.10.18 18:24')
        self.assertEqual(result['tracks'][-1].location, u'동작')
        self.assertEqual(result['tracks'][-1].phone1, u'010-1234-5678')

    @patch.object(HanjinParser, '_fetch')
    def test_hanjin_parser(self, _fetch):
        def fetch():
            with open('%s/hanjin.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('hanjin', 123456789123)
        result = armatis.find()

        self.assertEqual(result['parcel'].address, u'서울 송파 삼전')
        self.assertEqual(result['tracks'][-1].status, u'배송완료되었습니다.')
        self.assertEqual(result['tracks'][-1].time, u'2016-09-23 14:29')
        self.assertEqual(result['tracks'][-1].location, u'잠실2(대)')
        self.assertEqual(result['tracks'][-1].phone1, u'01012345678')

    @patch.object(LotteParser, '_fetch')
    def test_lotte_parser(self, _fetch):
        def fetch():
            with open('%s/lotte.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('lotte', 123456789123)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'물품을 받으셨습니다.')
        self.assertEqual(result['tracks'][-1].time, u'2016.12.22 --:--')
        self.assertEqual(result['tracks'][-1].location, u'고객')

    @patch.object(LogenParser, '_fetch')
    def test_logen_parser(self, _fetch):
        def fetch():
            with open('%s/logen.html' % DIR_MOCK_RESPONSES, 'r',
                      encoding='euc-kr') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('logen', 12345678912)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'배송완료')
        self.assertEqual(result['tracks'][-1].location, u'평택')
        self.assertEqual(result['tracks'][-1].phone1, u'010-1234-5678')

    @patch.object(KGBParser, '_fetch')
    def test_kgb_parser(self, _fetch):
        def fetch():
            with open('%s/kgb.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('kgb', 1234567891)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'완료')
        self.assertEqual(result['tracks'][-1].location, u'경기광주')
        self.assertEqual(result['tracks'][-1].time, u'20161227 22:05:03')
        self.assertEqual(result['tracks'][-1].phone1, u'왕** 010-1234-5678')

    @patch.object(EMSParser, '_fetch')
    def test_ems_parser(self, _fetch):
        def fetch():
            with open('%s/ems.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('ems', 'AA123456789BB')
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].time, u'2016-12-29')
        self.assertEqual(result['tracks'][-1].status, u'발송준비')

    @patch.object(GTXParser, '_fetch')
    def test_gtx_parser(self, _fetch):
        def fetch():
            with open('%s/gtx.html' % DIR_MOCK_RESPONSES, 'r',
                      encoding='euc-kr') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('gtx', 123456789123)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'배달완료')
        self.assertEqual(result['tracks'][-1].location, u'수원')
        self.assertEqual(result['tracks'][-1].time, u'2016.12.29 22:22')

    @patch.object(HapdongParser, '_fetch')
    def test_hapdong_parser(self, _fetch):
        def fetch():
            with open('%s/hapdong.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('hapdong', 12345678912)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'배달완료')
        self.assertEqual(result['tracks'][-1].location, u'충남금산추부563')
        self.assertEqual(result['tracks'][-1].time, u'2017-01-03 11:08')
        self.assertEqual(result['tracks'][-1].phone1, u'041-753-681')

    @patch.object(EPostParser, '_fetch')
    def test_epost_parser(self, _fetch):
        def fetch():
            with open('%s/epost.html' % DIR_MOCK_RESPONSES, 'r') as f:
                return f.read()
        _fetch.return_value = fetch()
        armatis = Armatis('epost', 1234567891234)
        result = armatis.find()

        self.assertEqual(result['tracks'][-1].status, u'배달완료')
        self.assertEqual(result['tracks'][-1].location, u'고객님의 상품이 배달완료 되었습니다.')
        self.assertEqual(result['tracks'][-1].time, u'2016.02.03 11:46')
