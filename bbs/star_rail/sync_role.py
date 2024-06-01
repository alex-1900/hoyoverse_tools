import html
import json
import os
import re
from urllib.parse import unquote

import pdfkit
import requests
from bs4 import BeautifulSoup

from bbs._functions import handle_response


class SyncRole:
    r"""
    同步角色信息
    """

    # _pdfkit_config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    _headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://bbs.mihoyo.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
    }

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.clear()
        self._session.headers.update(self._headers)
        self._pdf_html_buffer = f"""
            <html><head><meta charset="UTF-8" /><title>崩坏星穹铁道角色信息</title></head>
            <body>"""

    def _fetch_role(self, _content_id):
        url = 'https://api-static.mihoyo.com/common/blackboard/sr_wiki/v1/content/info'
        res = self._session.get(url, params={
            'app_sn': 'sr_wiki',
            'content_id': _content_id
        })

        return handle_response(res)

    def _get_role_struct(self, _content_id):
        _data = self._fetch_role(_content_id)
        _data = _data['content']
        return {
            'id': _data['id'],
            'role_name': _data['title'],
            # 'ext': json.decoder.JSONDecoder().decode(_data['ext']),
            'contents': _data['contents'],
        }

    def update_roles_data(self, _content_id):
        res = self._get_role_struct(_content_id)

        _html = f'<section><header>以下为角色[{res['role_name']}]的信息：</header>'
        _ext = ''
        for _content in res['contents']:
            _html = f'{_html}<h1>{_content['name']}</h1>{_content['text']}'
            _e = self._get_compute_points(_content['text'])
            if _e:
                _ext = f'{_ext}<p>{_e}</p>'

        self._pdf_html_buffer = f'{self._pdf_html_buffer}{_html}<p>角色行迹和角色属性信息：<br />{_ext}</p><footer>以上为角色[{res['role_name']}]的所有信息</footer></section>'

    def _get_compute_points(self, _text):
        _pattern = r'行迹面板中的行迹图标.+?data-data="([^"]+?)"'
        _match = re.search(_pattern, _text, re.M)
        _res = ''
        if _match:
            _points = _match.group(1)
            _html = unquote(_points)
            _json = BeautifulSoup(_html, 'html.parser').get_text()
            _data_dict = json.loads(_json)
            for _item_dict in _data_dict:
                if _item_dict['partKey'] == 'trace':
                    _role_id = _item_dict['data']['attr']['roleId']
                    _skill_html = self._get_skill_html(_item_dict['data']['attr']['points'], _role_id)
                    # print(_skill_html)
                    _res = f'{_res}<p>{_skill_html}</p>'
                if _item_dict['partKey'] == 'gainMethod':
                    _method_html = self._get_method_html(_item_dict['data']['gainMethod'])
                    _res = f'{_res}<p>{_method_html}</p>'
        return _res

    def _fetch_skill_list(self, _role_id, _point_id):
        url = 'https://api-static.mihoyo.com/common/blackboard/sr_wiki/v1/compute_point'
        res = self._session.get(url, params={
            'app_sn': 'sr_wiki',
            'point_id': _point_id,
            'role_id': _role_id
        })

        _resp = handle_response(res)
        _list = _resp['list']
        _html = f'共{len(_list)}级，'
        for _item in _list:
            _html = f'{_html}{_item['level']}级所需材料：'
            if len(_item['list']) == 0:
                _html = f'{_html}无'
            else:
                for _good in _item['list']:
                    _html = f'{_html}{_good['num']}{_good['item_name']}、'
            _html = f'{_html}；'
        return _html

    def _get_method_html(self, _json):
        _html = '<h1>角色属性：</h1><table><thead><tr><th>属性名称</th><th>详情</th></tr></thead><tbody>'
        for _method in _json:
            _html = f"""{_html}
                    <tr>
                    <td>{_method['key']}</td>
                    <td>{_method['value']}</td>
                    </tr>
                    """
        return f'{_html}</tbody></table>'

    def _get_skill_html(self, _json, _role_id):
        _html = '<h1>角色行迹：</h1><table><thead><tr><th>行迹类型</th><th>行迹名称</th><th>详情说明</th><th>升级材料</th></tr></thead><tbody>'
        for _key, skill in enumerate(_json):
            _skill_ext_html = self._fetch_skill_list(_role_id, _key + 1)
            _type_name = skill['name'].split()
            _html = f"""{_html}
            <tr>
            <td>{_type_name[0]}</td>
            <td>{_type_name[1]}</td>
            <td>{skill['desc']}</td>
            <td>{_skill_ext_html}</td>
            </tr>
            """
        return f'{_html}</tbody></table>'


    def create_roles_pdf(self, number):
        self._pdf_html_buffer = f'{self._pdf_html_buffer}</body></html>'

        _pdf_path = f'dist/star_role/roles/崩坏星穹铁道角色{number}.pdf'
        _directory = os.path.dirname(_pdf_path)

        os.makedirs(_directory) if not os.path.exists(_directory) else None
        os.remove(_pdf_path) if os.path.exists(_pdf_path) else None

        try:
            # , configuration=self._pdfkit_config
            pdfkit.from_string(self._pdf_html_buffer, _pdf_path)
        except Exception as e:
            pass
