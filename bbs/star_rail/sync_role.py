import json
import os

import pdfkit
import requests

from bbs._functions import handle_response


class SyncRole:
    r"""
    同步角色信息
    """

    _pdfkit_config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    _pdf_html_buffer = ''

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
        for _content in res['contents']:
            _html = f'{_html}<h1>{_content['name']}</h1>{_content['text']}'

        self._pdf_html_buffer = f'{self._pdf_html_buffer}{_html}<footer>以上为角色[{res['role_name']}]的所有信息</footer></section>'

    def create_roles_pdf(self):
        self._pdf_html_buffer = f'{self._pdf_html_buffer}</body></html>'

        _pdf_path = f'dist/star_role/roles/崩坏星穹铁道角色.pdf'
        _directory = os.path.dirname(_pdf_path)

        os.makedirs(_directory) if not os.path.exists(_directory) else None
        os.remove(_pdf_path) if os.path.exists(_pdf_path) else None

        pdfkit.from_string(self._pdf_html_buffer, _pdf_path, configuration=self._pdfkit_config)
