from typing import Any, Dict
import os
import requests
import json
from datetime import datetime
from src.utils.logger import error
from src.tools.auth.auth import Auth
from src.utils.logger import (
    info,
    error,
)

class Contract(Auth):
    def __init__(self):
        super().__init__()
        self.phpsessid = super().login()

    def upload(self, contract_attachment_path: str) -> Dict[str, Any]:
        """通达OA上传合同附件
    
        Args:
            contract_attachment_path: 合同附件路径

        Returns:
            Dict[str, Any]: 合同归档结果 - {
                "error": 错误信息,
                "data": {
                    "attach_id": 附件ID,
                    "attach_name": 附件名称,
                    "size": 附件大小,
                    "ctime": 附件创建时间
                }
            }
        """
        if not self.phpsessid:
            return {'error': '登录失败', 'data': {}}

        url = f"{self.base_url}/general/appbuilder/web/appdesign/appupload/upload"
        
        if not os.path.exists(contract_attachment_path):
            return {'error': f'文件不存在: {contract_attachment_path}', 'data': {}}
            
        if not contract_attachment_path.endswith('.pdf'):
            return {'error': '只支持PDF文件上传', 'data': {}}
            
        filename = os.path.basename(contract_attachment_path)
        file_size = os.path.getsize(contract_attachment_path)
        
        # 构建multipart form数据
        form_data = {
            'type': (None, 'application/pdf'),
            'is_delete': (None, 'false'),
            'is_down': (None, 'false'),
            'is_edit': (None, 'false'),
            'id': (None, 'WU_FILE_0'),
            'name': (None, filename),
            'lastModifiedDate': (None, datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)')),
            'size': (None, str(file_size)),
            'Filedata': (filename, open(contract_attachment_path, 'rb'), 'application/pdf')
        }

        # 设置请求头
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

        # 设置cookies
        cookies = {
            'PHPSESSID': self.phpsessid
        }

        try:
            # 发送请求
            response = requests.post(
                url,
                files=form_data,
                headers=headers,
                cookies=cookies,
                verify=False
            )
            json_response = response.json()

            response_data = {'error': None, 'data': {}}
            info(f"上传合同归档附件响应: {json_response}", console_output=False)
            if json_response.get('status') == 1 and json_response.get('data') and len(json_response['data']) > 0:
                response_data['data']['attach_id'] = json_response['data'][0].get('attach_id', '')
                response_data['data']['attach_name'] = json_response['data'][0].get('attach_name', '')
                response_data['data']['size'] = json_response['data'][0].get('size', '')
                response_data['data']['ctime'] = json_response['data'][0].get('ctime', '')
                info(f"获取到文件的attach_id: {response_data['data']['attach_id']}", console_output=False)
            
            return response_data
        except Exception as e:
            return {'error': str(e), 'data': {}}
