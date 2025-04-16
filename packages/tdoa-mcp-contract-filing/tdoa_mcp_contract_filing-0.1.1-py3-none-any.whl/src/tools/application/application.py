import os
from src.tools.auth.auth import Auth
import requests
import json
import re
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any
from src.utils.logger import (
    info,
    error,
)

class Application(Auth):
    def __init__(self, run_id: str, prcs_key_id: str, prcs_id: str, flow_prcs: str):
        super().__init__()
        self.phpsessid = super().login()
        self.flow_id = os.getenv("FLOW_ID", "")
        self.form_id = os.getenv("FORM_ID", "")
        self.field_id = os.getenv("FIELD_ID", "")
        self.run_id = run_id
        self.prcs_key_id = prcs_key_id
        self.prcs_id = prcs_id
        self.flow_prcs = flow_prcs

    def save_work(self, run_name: str, attach_id: str, attach_name: str, size: str, ctime: str) -> Dict[str, Any]:
        """保存工作
        
        Args:
            title: 标题
            attach_id: 附件ID
            attach_name: 附件名称
            size: 附件大小
            ctime: 附件创建时间

        Returns:
            Dict[str, Any]: 保存工作结果，包含以下字段：
                - error: 错误信息
        """
        if not self.phpsessid:
            return {"error": "未登录"}
        if not run_name:
            return {"error": "工作名称/文号不能为空"}
        if not attach_id:
            return {"error": "附件ID不能为空"}
        if not attach_name:
            return {"error": "附件名称不能为空"}
        if not size:
            return {"error": "附件大小不能为空"}
        if not ctime:
            return {"error": "附件创建时间不能为空"}
            
        # 获取run_key和did
        form_params = self._get_run_key_and_did()
        run_key = form_params["run_key"]
        did = form_params["did"]
        if run_key == "":
            return {"error": "无法获取run_key"}
        if did == "":
            return {"error": "无法获取did"}
        
        info(f"使用run_key: {run_key}, did: {did}", console_output=False)
            
        url = f"{self.base_url}/general/appbuilder/web/appcenter/appdata/save"
        
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/general/appbuilder/web/appcenter/appdata/handle",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": f"PHPSESSID={self.phpsessid}"
        }
        
        data = {
            "formId": self.form_id,
            "title": run_name,
            "run_id": self.run_id,
            "prcs_key_id": self.prcs_key_id,
            "prcs_id": self.prcs_id,
            "flow_prcs": self.flow_prcs,
            "type": "edit",
            "data[0][field_id]": self.field_id,
            "data[0][value][0][attach_id]": attach_id,
            "data[0][value][0][attach_name]": attach_name,
            "data[0][value][0][size]": size,
            "data[0][value][0][ctime]": ctime,
            "run_key": run_key,
            "did": did
        }
        
        info(f'保存工作参数: {data}', console_output=False)
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=data
            )
            result = response.json()
            info(f'保存工作响应: {result}', console_output=False)
            
            if isinstance(result, dict):
                if result.get("status", 0) == 1:
                    return {"error": None}
                else:
                    raise Exception("未知错误")
            else:
                raise Exception("响应格式错误")
                
        except Exception as e:
            error(f"保存工作失败: {e}", console_output=False)
            return {"error": str(e)}
        
        
    def turn_work(self, run_name: str) -> Dict[str, Any]:
        """通达OA转办工作
        
        Args:
            run_name: 工作名称/文号

        Returns:
            Dict[str, Any]: 转办结果，包含以下字段：
                - error: 错误信息
        """
        if not self.phpsessid:
            return {"error": "未登录"}
            
        # 获取run_key和did
        form_params = self._get_run_key_and_did()
        run_key = form_params["run_key"]
        did = form_params["did"]
        if run_key == "":
            return {"error": "无法获取run_key"}
        if did == "":
            return {"error": "无法获取did"}
        
        info(f"转办工作使用run_key: {run_key}, did: {did}", console_output=False)
        
        # 构建URL和请求头
        url = f"{self.base_url}/general/appbuilder/web/appcenter/appdata/submit"
        
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/general/appbuilder/web/appcenter/appdata/handle",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": f"PHPSESSID={self.phpsessid}"
        }
        
        # 构建请求数据
        data = {
            "formId": self.form_id,
            "run_id": self.run_id,
            "prcs_key_id": self.prcs_key_id,
            "prcs_id": self.prcs_id,
            "flow_prcs": self.flow_prcs,
            "type": "edit",
            "next_prcs[]": "0",
            "next_user[0][prcs_op_user]": "",
            "next_user[0][prcs_user]": "",
            "next_user[0][prcs_type]": "",
            "timeout[0]": "0",
            "topflag[0]": "0",
            "prcs_back[0]": "",
            "free_item[0]": "",
            "free_form_item[0]": "",
            "sms_content": "您有新的工作需要办理，流水号：" + self.run_id + "，工作名称/文号：" + run_name,
            "info_str_arr[next][0][sms]": "1",
            "info_str_arr[next][0][sms_display]": "1",
            "info_str_arr[next][0][mobile]": "0",
            "info_str_arr[next][0][mobile_display]": "1",
            "info_str_arr[next][0][email]": "0",
            "info_str_arr[next][0][email_display]": "1",
            "info_str_arr[create][0][sms]": "0",
            "info_str_arr[create][0][sms_display]": "1",
            "info_str_arr[create][0][mobile]": "0",
            "info_str_arr[create][0][mobile_display]": "1",
            "info_str_arr[create][0][email]": "0",
            "info_str_arr[create][0][email_display]": "1",
            "info_str_arr[managers][0][sms]": "0",
            "info_str_arr[managers][0][sms_display]": "1",
            "info_str_arr[managers][0][mobile]": "0",
            "info_str_arr[managers][0][mobile_display]": "1",
            "info_str_arr[managers][0][email]": "0",
            "info_str_arr[managers][0][email_display]": "1",
            "run_key": run_key,
            "did": did
        }
        
        info(f'转办工作请求参数: {data}', console_output=False)
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=data
            )
            result = response.json()
            info(f'转办工作响应: {result}', console_output=False)
            
            if isinstance(result, dict):
                if result.get("status", 0) == 1:
                    return {"error": None}
                else:
                    raise Exception("未知错误")
            else:
                raise Exception("响应格式错误")
                
        except Exception as e:
            error(f"转办工作失败: {e}", console_output=False)
            return {"error": str(e)}
    
    def _get_run_key_and_did(self) -> Dict[str, str]:
        """获取应用中心搭配流程的run_key和did
        
        Returns:
            Dict[str, str]: 包含run_key和did的字典，包含以下字段：
                - run_key
                - did
        """
        # 设置请求头
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": f"PHPSESSID={self.phpsessid}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        
        # 构建URL
        url = f"{self.base_url}/general/approve_center/list/input_form/"
        params = {
            "actionType": "handle",
            "MENU_FLAG": "",
            "RUN_ID": self.run_id,
            "PRCS_KEY_ID": self.prcs_key_id,
            "FLOW_ID": self.flow_id,
            "PRCS_ID": self.prcs_id,
            "FLOW_PRCS": self.flow_prcs
        }
        
        try:
            # 发送请求但不自动跟随重定向
            response = requests.get(url, params=params, headers=headers, allow_redirects=False)
            info(f"获取run_key请求状态码: {response.status_code}", console_output=False)
            
            # 初始化默认返回值
            result = {"run_key": "", "did": ""}

            # 检查是否为302重定向
            if response.status_code == 302:
                # 获取重定向URL
                redirect_url = response.headers.get('Location')
                redirect_url = self.base_url + redirect_url
                info(f"获取到重定向URL: {redirect_url}", console_output=False)
                
                # 从重定向URL中解析did参数
                parsed_url = urllib.parse.urlparse(redirect_url)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                # 获取did参数
                if 'did' in query_params:
                    did = query_params['did'][0]
                    result["did"] = did
                    info(f"从重定向URL中获取到did: {did}", console_output=False)
                
                if redirect_url:
                    # 发送请求到重定向URL
                    redirect_response = requests.get(redirect_url, headers=headers)
                    info(f"重定向请求状态码: {redirect_response.status_code}", console_output=False)
                    
                    if redirect_response.status_code == 200:
                        # 从响应内容中提取run_key
                        run_key_pattern = r'run_key\s*=\s*["\']([\d]+)["\']'
                        match = re.search(run_key_pattern, redirect_response.text)
                        
                        if match:
                            run_key = match.group(1)
                            result["run_key"] = run_key
                            info(f"从重定向响应中获取到run_key: {run_key}", console_output=False)
            
            if run_key == "":
                raise Exception("无法获取run_key")
            if did == "":
                raise Exception("无法获取did")
            
            return result
                
        except Exception as e:
            error(f"获取run_key和did异常: {str(e)}", console_output=False)
            return {"run_key": "", "did": ""}