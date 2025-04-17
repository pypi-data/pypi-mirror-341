"""
콘솔 스크립트 entry – 'dizest_MCP' 명령은 여기 main()을 호출.
별도 인자 없이 FastMCP 서버를 바로 실행한다.
"""
from dizest_MCP.mcp_server import run

def main() -> None:
    print("Starting FastMCP server ...  (Ctrl‑C to stop)")
    try:
        run()               # 내부에서 툴들이 이미 import 되어 있음
    except KeyboardInterrupt:
        print("\nServer stopped.")
