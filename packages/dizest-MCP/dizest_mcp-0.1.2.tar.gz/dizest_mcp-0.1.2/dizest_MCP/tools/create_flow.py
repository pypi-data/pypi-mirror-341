import json, os, uuid
from dizest_MCP.mcp_server import mcp
import uuid
import os


@mcp.tool()
def create_flow(code_blocks, title, file_path=None, connections=None, connection_type="mixed"):
    """
    코드 블록과 제목, file_path를 받아 플로우 dwp을 생성 또는 업데이트합니다.
    
    Args:
        code_blocks: 앱 ID를 키로 하는 코드 블록 딕셔너리
        title: 플로우 제목
        file_path: 파일 저장 경로
        connections: 앱 간 연결을 정의하는 딕셔너리
            - 기본 형식: {"app_id": ["target_app_id1", "target_app_id2"]}
            - 상세 형식: {"app_id": [{"target": "target_app_id", "output": "output_name", "input": "input_name"}]}
        connection_type: 연결 유형 - "serial"(직렬), "parallel"(병렬), "mixed"(혼합)
    """
    
    # connections 파라미터가 None이면 빈 딕셔너리로 초기화
    connections = connections or {}

    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    flow_data = json.load(f)
                except json.JSONDecodeError:
                    flow_data = None
            if not flow_data:
                flow_data = {
                    "apps": {},
                    "description": "",
                    "featured": "",
                    "flow": {},
                    "logo": "",
                    "title": title,
                    "version": "",
                    "visibility": "private",
                    "extra": {},
                    "favorite": "0",
                    "category": ""
                }
        else:
            flow_data = {
                "apps": {},
                "description": "",
                "featured": "",
                "flow": {},
                "logo": "",
                "title": title,
                "version": "",
                "visibility": "private",
                "extra": {},
                "favorite": "0",
                "category": ""
            }
    except Exception as e:
        print(f"파일 읽기 오류: {e}, 새 flow_data 생성")
        flow_data = {
            "apps": {},
            "description": "",
            "featured": "",
            "flow": {},
            "logo": "",
            "title": title,
            "version": "",
            "visibility": "private",
            "extra": {},
            "favorite": "0",
            "category": ""
        }
    
    # 기존 앱 및 플로우 데이터 초기화 (중복 방지)
    flow_data["apps"] = {}
    flow_data["flow"] = {}
    
    # 노드 위치 설정
    node_spacing_x = 300
    node_spacing_y = 250
    max_nodes_per_row = 3
    
    # 각 앱의 노드 ID를 저장할 딕셔너리 초기화
    app_to_node_id = {}
    app_ids = list(code_blocks['apps'].keys())
    
    # 앱 추가
    for idx, app_id in enumerate(app_ids):
        app_info = code_blocks['apps'][app_id]
        flow_data["apps"][app_id] = {
            "id": app_id,
            "title": app_info.get("title", f"App {app_id}"),
            "version": "1.0.0",
            "description": "",
            "cdn": {"js": [], "css": []},
            "inputs": app_info.get("inputs", []),
            "outputs": app_info.get("outputs", []),
            "code": app_info.get("code", "# 코드 없음"),
            "api": "",
            "html": "",
            "js": "",
            "css": ""
        }
        
        node_id = f"{app_id}-{int(uuid.uuid4().int % 1e16)}"
        app_to_node_id[app_id] = node_id
        
        # 출력 설정
        outputs = {}
        for output in app_info.get("outputs", []):
            outputs[output["name"]] = {"connections": []}
            
        # 입력 설정
        inputs = {}
        for input_data in app_info.get("inputs", []):
            inputs[input_data["name"]] = {"connections": []}
        
        # 노드 위치 계산
        row = idx // max_nodes_per_row
        col = idx % max_nodes_per_row
        
        if connection_type == "parallel":
            if idx == 0:
                pos_x = 600
                pos_y = 200
            else:
                pos_x = 300 + (col * node_spacing_x)
                pos_y = 450
        else:
            pos_x = 300 + (col * node_spacing_x)
            pos_y = 200 + (row * node_spacing_y)
        
        # 노드 추가
        flow_data["flow"][node_id] = {
            "app_id": app_id,
            "class": "",
            "data": {},
            "active": True,
            "description": "",
            "id": node_id,
            "inputs": inputs,
            "name": "",
            "outputs": outputs,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "typenode": False,
            "height": 270,
            "width": 260
        }
    
    # 개선된 연결 로직
    if not connections:
        if connection_type == "parallel" and len(app_ids) > 1:
            source_app_id = app_ids[0]
            source_node_id = app_to_node_id[source_app_id]
            source_node = flow_data["flow"][source_node_id]
            source_app_info = code_blocks['apps'][source_app_id]
            
            if source_app_info.get("outputs", []):
                output_types = {}
                for output in source_app_info.get("outputs", []):
                    output_name = output["name"]
                    output_type = output.get("type", "output")
                    if output_type not in output_types:
                        output_types[output_type] = []
                    output_types[output_type].append(output_name)
                
                for target_app_id in app_ids[1:]:
                    target_node_id = app_to_node_id[target_app_id]
                    target_node = flow_data["flow"][target_node_id]
                    target_app_info = code_blocks['apps'][target_app_id]
                    
                    target_inputs = target_app_info.get("inputs", [])
                    matched = False
                    for target_input in target_inputs:
                        target_input_name = target_input["name"]
                        target_input_type = target_input.get("type", "output")
                        
                        if target_input_type in output_types and output_types[target_input_type]:
                            source_output_name = output_types[target_input_type][0]
                            
                            # 소스 노드 출력 연결
                            source_node["outputs"][source_output_name]["connections"].append({
                                "node": target_node_id,
                                "output": target_input_name
                            })
                            
                            # 타겟 노드 입력 연결
                            target_node["inputs"][target_input_name]["connections"].append({
                                "node": source_node_id,
                                "input": source_output_name
                            })
                            
                            matched = True
                            break
                    
                    if not matched and target_inputs and source_app_info.get("outputs", []):
                        source_output_name = source_app_info["outputs"][0]["name"]
                        target_input_name = target_inputs[0]["name"]
                        
                        source_node["outputs"][source_output_name]["connections"].append({
                            "node": target_node_id,
                            "output": target_input_name
                        })
                        
                        target_node["inputs"][target_input_name]["connections"].append({
                            "node": source_node_id,
                            "input": source_output_name
                        })
        
        elif connection_type == "serial" or (connection_type == "mixed" and len(app_ids) > 1):
            for i in range(len(app_ids) - 1):
                current_app_id = app_ids[i]
                next_app_id = app_ids[i + 1]
                
                current_node_id = app_to_node_id[current_app_id]
                next_node_id = app_to_node_id[next_app_id]
                
                current_node = flow_data["flow"][current_node_id]
                next_node = flow_data["flow"][next_node_id]
                
                current_app_info = code_blocks['apps'][current_app_id]
                next_app_info = code_blocks['apps'][next_app_id]
                
                current_outputs = current_app_info.get("outputs", [])
                next_inputs = next_app_info.get("inputs", [])
                
                if current_outputs and next_inputs:
                    matches = []
                    for out in current_outputs:
                        out_name = out["name"]
                        for inp in next_inputs:
                            inp_name = inp["name"]
                            if out_name == inp_name:
                                matches.append((out_name, inp_name, 3))
                            elif out_name in inp_name or inp_name in out_name:
                                matches.append((out_name, inp_name, 2))
                    
                    if not matches:
                        matches.append((current_outputs[0]["name"], next_inputs[0]["name"], 1))
                    
                    matches.sort(key=lambda x: x[2], reverse=True)
                    output_key, input_key, _ = matches[0]
                    
                    # 현재 노드 출력 연결
                    current_node["outputs"][output_key]["connections"].append({
                        "node": next_node_id,
                        "output": input_key
                    })
                    
                    # 다음 노드 입력 연결
                    next_node["inputs"][input_key]["connections"].append({
                        "node": current_node_id,
                        "input": output_key
                    })
    else:
        for source_app_id, targets in connections.items():
            if source_app_id not in app_to_node_id:
                continue
                
            source_node_id = app_to_node_id[source_app_id]
            source_node = flow_data["flow"][source_node_id]
            source_app_info = code_blocks['apps'][source_app_id]
            
            if targets and isinstance(targets[0], str):
                for target_app_id in targets:
                    if target_app_id not in app_to_node_id:
                        continue
                        
                    target_node_id = app_to_node_id[target_app_id]
                    target_node = flow_data["flow"][target_node_id]
                    target_app_info = code_blocks['apps'][target_app_id]
                    
                    source_outputs = source_app_info.get("outputs", [])
                    target_inputs = target_app_info.get("inputs", [])
                    
                    if source_outputs and target_inputs:
                        match_found = False
                        for out in source_outputs:
                            out_name = out["name"]
                            for inp in target_inputs:
                                inp_name = inp["name"]
                                if out_name == inp_name or out_name in inp_name or inp_name in out_name:
                                    source_node["outputs"][out_name]["connections"].append({
                                        "node": target_node_id,
                                        "output": inp_name
                                    })
                                    
                                    target_node["inputs"][inp_name]["connections"].append({
                                        "node": source_node_id,
                                        "input": out_name
                                    })
                                    
                                    match_found = True
                                    break
                            if match_found:
                                break
                        
                        if not match_found:
                            source_output_name = source_outputs[0]["name"]
                            target_input_name = target_inputs[0]["name"]
                            
                            source_node["outputs"][source_output_name]["connections"].append({
                                "node": target_node_id,
                                "output": target_input_name
                            })
                            
                            target_node["inputs"][target_input_name]["connections"].append({
                                "node": source_node_id,
                                "input": source_output_name
                            })
            else:
                for connection_info in targets:
                    target_app_id = connection_info.get("target")
                    output_name = connection_info.get("output")
                    input_name = connection_info.get("input")
                    
                    if target_app_id not in app_to_node_id:
                        continue
                    
                    target_node_id = app_to_node_id[target_app_id]
                    target_node = flow_data["flow"][target_node_id]
                    target_app_info = code_blocks['apps'][target_app_id]
                    
                    if not output_name:
                        source_outputs = source_app_info.get("outputs", [])
                        if source_outputs:
                            output_name = source_outputs[0]["name"]
                    
                    if not input_name:
                        target_inputs = target_app_info.get("inputs", [])
                        if target_inputs:
                            input_name = target_inputs[0]["name"]
                    
                    if output_name in source_node["outputs"] and input_name in target_node["inputs"]:
                        source_node["outputs"][output_name]["connections"].append({
                            "node": target_node_id,
                            "output": input_name
                        })
                        
                        target_node["inputs"][input_name]["connections"].append({
                            "node": source_node_id,
                            "input": output_name
                        })
    
    # JSON 생성
    flow_data["id"] = f"{title}.dwp"
    flow_data["kernel_id"] = f"root-{str(uuid.uuid4())}"
    flow_data["executable"] = None
    flow_data["executable_name"] = "base"
    
    flow_json = json.dumps(flow_data, indent=2, ensure_ascii=False)
    
    # 파일 저장
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(flow_json)
            return f"플로우가 {file_path}에 저장 및 업데이트되었습니다. 연결 유형: {connection_type}"
        except Exception as e:
            return f"파일 저장 중 오류 발생: {e}\n{flow_json}"
    
    return flow_json