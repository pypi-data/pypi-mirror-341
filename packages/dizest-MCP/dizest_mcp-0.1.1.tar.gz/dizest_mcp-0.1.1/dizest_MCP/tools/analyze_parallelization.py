import json
import re
from langchain_openai import ChatOpenAI
from dizest_MCP.mcp_server import mcp

@mcp.tool()
# 병렬성 판단 도구
def analyze_parallelization(query: str) -> dict:
    """
    사용자 쿼리를 분석하여 병렬 처리가 필요한지 판단합니다.
    
    Args:
        query: 사용자 쿼리
    """
    prompt = """
    아래 사용자의 요청을 분석하여 병렬 실행이 더 적합한지, 직렬 실행이 더 적합한지 판단하세요.
    
    병렬 실행이 적합한 경우:
    - 여러 독립적인 작업을 동시에 실행해야 할 때
    - 같은 입력에 대해 여러 다른 처리를 해야 할 때
    - 알고리즘, 방법 등을 비교해야 할 때
    - "병렬", "동시에", "비교", "각각" 등의 키워드가 명시적으로 있을 때
    
    직렬 실행이 적합한 경우:
    - 한 작업의 결과가 다음 작업의 입력으로 필요할 때
    - 단계별 처리가 필요한 경우
    - "순차적", "단계별", "연속" 등의 키워드가 있을 때
    
    요청: {query}
    
    분석 결과를 다음 형식으로 제공하세요:
    ```json
    {
      "connection_type": "serial" 또는 "parallel",
      "reason": "선택한 이유에 대한 간략한 설명"
    }
    ```
    """
    
    formatted_prompt = prompt.format(query=query)
    analysis_response = model.invoke(formatted_prompt)
    
    try:
        # 응답에서 JSON 형식 찾기
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', analysis_response.content, re.DOTALL)
        
        if json_match:
            analysis_result = json.loads(json_match.group(1))
        else:
            # JSON 형식이 없으면 전체 텍스트에서 파싱 시도
            analysis_result = json.loads(analysis_response.content)
            
        return analysis_result
    except Exception as e:
        #print(f"병렬성 분석 오류: {e}")
        # 기본값은 mixed로 설정
        return {"connection_type": "mixed", "reason": "분석 중 오류 발생"}
