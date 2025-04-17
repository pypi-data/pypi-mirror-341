import os
import json
from dizest_MCP.mcp_server import mcp

@mcp.tool()
def analyze_existing_file(file_path: str) -> dict:
    """
    기존 파일의 내용을 읽고 분석합니다.
    
    Args:
        file_path: 분석할 파일 경로
    
    Returns:
        파일 분석 결과 또는 없을 경우 빈 딕셔너리
    """
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    flow_data = json.load(f)
                    return {
                        "file_exists": True,
                        "flow_data": flow_data,
                        "analysis": "파일이 성공적으로 로드되었습니다."
                    }
                except json.JSONDecodeError:
                    return {
                        "file_exists": True,
                        "flow_data": None,
                        "analysis": "파일이 존재하지만 유효한 JSON 형식이 아닙니다."
                    }
        else:
            return {
                "file_exists": False,
                "flow_data": None, 
                "analysis": "파일이 존재하지 않습니다. 새 파일을 생성합니다."
            }
    except Exception as e:
        return {
            "error": str(e),
            "file_exists": False,
            "flow_data": None,
            "analysis": f"파일 분석 중 오류 발생: {e}"
        }