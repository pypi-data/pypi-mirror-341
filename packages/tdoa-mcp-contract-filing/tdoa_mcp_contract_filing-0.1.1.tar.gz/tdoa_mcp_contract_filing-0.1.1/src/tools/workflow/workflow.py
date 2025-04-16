
import os
import re
from typing import Any, Dict, List
import requests
from src.tools.auth.auth import Auth
from src.utils.logger import (
    info,
    error,
)

class Workflow(Auth):
    def __init__(self):
        super().__init__()
        self.phpsessid = super().login()
        self.flow_id = os.getenv("FLOW_ID", "")

    def get_todo_work_list(self) -> List[Dict[str, Any]]:
        """获取通达OA系统中的待办工作列表
    
        Returns:
            List[Dict[str, Any]]: 待办工作列表 - [{
                "run_id": 流程实例ID,
                "prcs_key_id": 流程实例主键ID,
                "flow_id": 流程ID,
                "prcs_id": 实际步骤ID,
                "flow_prcs": 设计步骤ID,
                "run_name": 工作名称/文号,
                "prcs_name": 当前步骤名称
            }]
        """
        if not self.phpsessid:
            return []

        url = f"{self.base_url}/general/approve_center/list/data/getdata.php"
        
        params = {
            "action": "list_mywork",
            "pageType": "todo",
            "searchType": "adv"
        }
        if self.flow_id:
            params["flow_id"] = self.flow_id
            
        info(f'获取待办列表参数: {params}', console_output=False)
        
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "origin": self.base_url,
            "referer": f"{self.base_url}/general/approve_center/list/todo.php",
            "cookie": f"PHPSESSID={self.phpsessid}",
        }
        
        data = {
            "_search": "false",
            "rows": 100,
            "page": 1,
            "sidx": "run_id",
            "sord": "desc"
        }
        
        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                data=data
            )
            result = response.json()

            info(f'获取待办列表响应: {result}', console_output=False)
            # 解析数据
            todo_list = []
            if result.get("rows"):
                for row in result["rows"]:
                    if row.get("cell") and len(row["cell"]) > 0:
                        # 使用正则表达式匹配handle_work函数的参数
                        handle_pattern = r"handle_work\('', '(\d+)', '(\d+)', '(\d+)', '(\d+)', '(\d+)'\).*?>(.*?)<\/a>"
                        handle_match = re.search(handle_pattern, row["cell"][1])
                        
                        # 匹配步骤名称
                        prcs_pattern = r"flow_view\('.*?'\).*?>第\d+步：(.*?)<\/a>"
                        prcs_match = re.search(prcs_pattern, row["cell"][2])

                        prcs_name = prcs_match.group(1) if prcs_match else ""
                        if prcs_name != "合同归档":
                            continue
                        if handle_match:
                            todo_item = {
                                "run_id": handle_match.group(1),
                                "prcs_key_id": handle_match.group(2),
                                "flow_id": handle_match.group(3),
                                "prcs_id": handle_match.group(4),
                                "flow_prcs": handle_match.group(5),
                                "run_name": handle_match.group(6),
                                "prcs_name": prcs_name
                            }
                            todo_list.append(todo_item)
            
            return todo_list
            
        except Exception as e:
            error(f"获取待办列表失败: {str(e)}", console_output=False)
            return []
        