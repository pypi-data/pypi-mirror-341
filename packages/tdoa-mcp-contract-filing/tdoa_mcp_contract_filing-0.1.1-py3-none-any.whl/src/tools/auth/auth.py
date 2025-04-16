import os
import base64
import requests
from bs4 import BeautifulSoup

class Auth:
    def __init__(self):
        self.base_url = os.getenv("OA_URL", "")
        self.username = os.getenv("LOGIN_USERNAME", "")
        self.password = os.getenv("LOGIN_PASSWORD", "")

        # 密码base64解码
        self.password = base64.b64decode(self.password).decode()

    def login(self) -> str:
        """通达OA登录
        
        Returns:
            str: PHPSESSID
        """
        url = self.base_url + "/logincheck.php"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        data = {
            "UNAME": self.username,
            "PASSWORD": self.password,
            "encode_type": "1"
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            phpsessid = response.cookies.get("PHPSESSID")
            if phpsessid:
                return phpsessid
            else:
                return ""
        else:
            return ""

    def get_csrftoken(self, phpsessid: str) -> str:
        """获取通达OA CSRF Token
        
        Args:
            phpsessid: PHPSESSID

        Returns:
            str: CSRF Token
        """
        url = self.base_url + "/general/email/new/"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "proxy-connection": "keep-alive",
            "upgrade-insecure-requests": "1",
            "cookie": f"PHPSESSID={phpsessid}",
            "Referer": f"{self.base_url}/general/email/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_token_input:
                csrf_token = csrf_token_input['value']
                return csrf_token
            else:
                return ""
        else:
            return ""