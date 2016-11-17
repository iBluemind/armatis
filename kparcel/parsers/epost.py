# -*- coding: utf-8 -*-


from kparcel.models import Track, Parcel
from kparcel.parser import Parser, ParserRequest


class EPostParser(Parser):
    def __init__(self, invoice_number, auth_key):
        super(EPostParser, self).__init__(invoice_number)
        self.auth_key = auth_key
        parser_request = ParserRequest()
        parser_request.url = 'http://openapi.epost.go.kr/trace/retrieveLongitudinalService/' \
                             'retrieveLongitudinalService/getLongitudinalDomesticList?' \
                             'ServiceKey=%s&rgist=%s' % (auth_key, self.invoice_number)
        self.parser_request = parser_request

    def parse(self, parser, response):
        if self.auth_key is None:
            raise EnvironmentError('The auth_key must be set!')
        longitudinal_domestic_list_response = parser.find('longitudinaldomesticlistresponse')

        cmm_msg_header = longitudinal_domestic_list_response.find('cmmmsgheader')
        request_msg_id = cmm_msg_header.find('requestmsgid').string
        response_msg_id = cmm_msg_header.find('responsemsgid').string
        response_time = cmm_msg_header.find('responsetime').string
        success_y_n = cmm_msg_header.find('successyn').string
        return_code = cmm_msg_header.find('returncode').string
        err_msg = cmm_msg_header.find('errmsg').string

        addrse_nm = longitudinal_domestic_list_response.find('addrsenm').string #수취인
        applcnt_nm = longitudinal_domestic_list_response.find('applcntnm').string   #발송인
        dlvy_de = longitudinal_domestic_list_response.find('dlvyde').string #배달일자
        dlvy_sttus = longitudinal_domestic_list_response.find('dlvysttus').string   #배달상태

        longitudinal_domestic_list = longitudinal_domestic_list_response.find_all('longitudinaldomesticlist')    #종적목록
        for longitudinal_domestic in longitudinal_domestic_list:
            dlvy_date = longitudinal_domestic.find('dlvydate').string #날짜
            dlvy_time = longitudinal_domestic.find('dlvytime').string #시간
            now_lc = longitudinal_domestic.find('nowlc').string   #현재위치
            process_sttus = longitudinal_domestic.find('processsttus').string #처리현황
            detail_dc = longitudinal_domestic.find('detaildc').string #상세설명

            time = dlvy_date + ' ' + dlvy_time

            track = Track()
            track.time = time
            track.location = now_lc
            track.status = process_sttus
            self.add_track(track)

        pstmtr_knd = longitudinal_domestic_list_response.find('pstmtrknd').string   #우편물종류
        rgist = longitudinal_domestic_list_response.find('rgist').string   #등기번호
        trtmnt_se = longitudinal_domestic_list_response.find('trtmntse').string #취급구분

        parcel = Parcel()
        parcel.sender = applcnt_nm
        parcel.receiver = addrse_nm
        parcel.note = pstmtr_knd
        self.parcel = parcel

