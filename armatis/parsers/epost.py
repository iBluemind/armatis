# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class EPostParser(Parser):
    def __init__(self, invoice_number, config):
        super(EPostParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://openapi.epost.go.kr/trace/retrieveLongitudinalService/' \
                                           'retrieveLongitudinalService/getLongitudinalDomesticList?' \
                                           'ServiceKey=%s&rgist=%s' %
                                           (config['EPOST_AUTH_KEY'], self.invoice_number))
        self.add_request(parser_request)

    def parse(self, parser):
        longitudinal_domestic_list_response = parser.find('longitudinaldomesticlistresponse')

        cmm_msg_header = longitudinal_domestic_list_response.find('cmmmsgheader')
        request_msg_id = cmm_msg_header.find('requestmsgid').string
        response_msg_id = cmm_msg_header.find('responsemsgid').string
        response_time = cmm_msg_header.find('responsetime').string
        success_y_n = cmm_msg_header.find('successyn').string
        return_code = cmm_msg_header.find('returncode').string
        err_msg = cmm_msg_header.find('errmsg').string

        # 수취인
        addrse_nm = longitudinal_domestic_list_response.find('addrsenm').string
        # 발송인
        applcnt_nm = longitudinal_domestic_list_response.find('applcntnm').string
        # 배달일자
        dlvy_de = longitudinal_domestic_list_response.find('dlvyde').string
        # 배달상태
        dlvy_sttus = longitudinal_domestic_list_response.find('dlvysttus').string

        # 종적목록
        longitudinal_domestic_list = longitudinal_domestic_list_response.find_all('longitudinaldomesticlist')
        for longitudinal_domestic in longitudinal_domestic_list:
            # 날짜
            dlvy_date = longitudinal_domestic.find('dlvydate').string
            # 시간
            dlvy_time = longitudinal_domestic.find('dlvytime').string
            # 현재위치
            now_lc = longitudinal_domestic.find('nowlc').string
            # 처리현황
            process_sttus = longitudinal_domestic.find('processsttus').string
            # 상세설명
            detail_dc = longitudinal_domestic.find('detaildc').string

            time = dlvy_date + ' ' + dlvy_time

            track = Track()
            track.time = time
            track.location = now_lc
            track.status = process_sttus
            self.add_track(track)

        # 우편물종류
        pstmtr_knd = longitudinal_domestic_list_response.find('pstmtrknd').string
        # 등기번호
        rgist = longitudinal_domestic_list_response.find('rgist').string
        # 취급구분
        trtmnt_se = longitudinal_domestic_list_response.find('trtmntse').string

        parcel = Parcel()
        parcel.sender = applcnt_nm
        parcel.receiver = addrse_nm
        parcel.note = pstmtr_knd
        self.parcel = parcel
