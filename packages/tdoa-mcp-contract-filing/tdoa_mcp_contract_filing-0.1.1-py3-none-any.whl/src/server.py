import time
from fastmcp import FastMCP
from typing import Dict, Any, List

from src.tools.contract import Contract
from src.tools.application import Application
from src.tools.workflow import Workflow

# Create an MCP server
mcp = FastMCP(
    "tdoa-mcp",
    description="Tongda OA integration through the Model Context Protocol",
)

@mcp.tool()
def get_todo_work_list() -> List[Dict[str, Any]]:
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
    workflow = Workflow()
    return workflow.get_todo_work_list()

@mcp.tool()
def upload_contract_attachment(contract_attachment_path: str) -> Dict[str, Any]:
    """通达OA上传合同附件
    
    Args:
        contract_attachment_path: 合同附件路径

    Returns:
        Dict[str, Any]: 合同归档结果 - {
            "error": 错误信息，如果上传成功则返回None,
            "data": {
                "attach_id": 附件ID,
                "attach_name": 附件名称,
                "size": 附件大小,
                "ctime": 附件创建时间
            }
        }
    """
    contract = Contract()
    return contract.upload(contract_attachment_path)

@mcp.tool()
def save_work(run_id: str, prcs_key_id: str, prcs_id: str, flow_prcs: str, run_name: str, attach_id: str, attach_name: str, size: str, ctime: str) -> str:
    """通达OA保存工作
    
    Args:
        run_id: 流程实例ID
        prcs_key_id: 流程实例主键ID
        prcs_id: 实际步骤ID
        flow_prcs: 设计步骤ID
        run_name: 工作名称/文号
        attach_id: 附件ID
        attach_name: 附件名称
        size: 附件大小
        ctime: 附件创建时间

    Returns:
        Dict[str, Any]: 保存工作结果 - {
            "error": 错误信息，如果保存成功则返回None
        }
    """
    application = Application(run_id, prcs_key_id, prcs_id, flow_prcs)
    return application.save_work(run_name, attach_id, attach_name, size, ctime)

@mcp.tool()
def turn_work(run_id: str, prcs_key_id: str, prcs_id: str, flow_prcs: str, run_name: str) -> Dict[str, Any]:
    """通达OA转办工作
    
    Args:
        run_id: 流程实例ID
        prcs_key_id: 流程实例主键ID
        prcs_id: 实际步骤ID
        flow_prcs: 设计步骤ID
        run_name: 工作名称/文号
    Returns:
        Dict[str, Any]: 转办工作结果 - {
            "error": 错误信息，如果转办成功则返回None
        }
    """
    application = Application(run_id, prcs_key_id, prcs_id, flow_prcs)
    return application.turn_work(run_name)

@mcp.tool()
def get_current_time() -> str:
    """获取当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# @mcp.prompt()
# def contract_filing() -> str:
#     """通达OA合同归档流程
#     """
#     return  """
#     通达OA合同归档流程如下：
#     1. 调用get_todo_work_list工具获取待办工作列表，匹配待上传的通达OA合同扫描件名称，是否在待办工作列表中（匹配依据为工作名称/文号）
#     2. 如果匹配到，则调用upload_contract_attachment工具上传合同附件，并返回附件ID、附件名称、附件大小、附件创建时间
#     3. 调用save_work工具保存工作，并返回保存结果，调用参数为待办工作列表中匹配到的数据，包括：
#         - run_id: 流程实例ID
#         - prcs_key_id: 流程实例主键ID
#         - prcs_id: 实际步骤ID
#         - flow_prcs: 设计步骤ID
#         - run_name: 工作名称/文号
#         以及调用upload_contract_attachment工具返回的数据，包括：
#         - attach_id: 附件ID
#         - attach_name: 附件名称
#         - size: 附件大小
#         - ctime: 附件创建时间
#     4. 调用turn_work工具转办工作，并返回转办结果，调用参数为待办工作列表中匹配到的数据，包括：
#         - run_id: 流程实例ID
#         - prcs_key_id: 流程实例主键ID
#         - prcs_id: 实际步骤ID
#         - flow_prcs: 设计步骤ID
#         - run_name: 工作名称/文号
#     """

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()