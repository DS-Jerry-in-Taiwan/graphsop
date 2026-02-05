import pytest

def parse_mermaid_states(mermaid_code):
    """
    粗略解析 mermaid 狀態圖，回傳節點與邊的集合
    """
    nodes = set()
    edges = set()
    for line in mermaid_code.splitlines():
        line = line.strip()
        if "-->" in line:
            parts = line.split("-->")
            src = parts[0].strip()
            dst = parts[1].split(":")[0].strip() if ":" in parts[1] else parts[1].strip()
            nodes.add(src)
            nodes.add(dst)
            edges.add((src, dst))
    return nodes, edges

@pytest.fixture(scope="module")
def workflow_mermaid():
    with open("src/logic/workflow_design.md", encoding="utf-8") as f:
        lines = f.readlines()
    # 找到 mermaid 區塊
    in_code = False
    code = []
    for line in lines:
        if "```mermaid" in line:
            in_code = True
            continue
        if in_code and "```" in line:
            break
        if in_code:
            code.append(line)
    return "".join(code)

def test_check_safety_precedes_execute(workflow_mermaid):
    nodes, edges = parse_mermaid_states(workflow_mermaid)
    # 檢查 Check_Safety 必須在 Execute 之前
    assert ("Plan", "Check_Safety") in edges
    assert ("Check_Safety", "Execute") in edges

def test_check_safety_has_failure_path(workflow_mermaid):
    nodes, edges = parse_mermaid_states(workflow_mermaid)
    # 檢查 Check_Safety 有失敗路徑到 Error
    assert ("Check_Safety", "Error") in edges

def test_no_direct_plan_to_execute(workflow_mermaid):
    nodes, edges = parse_mermaid_states(workflow_mermaid)
    # 不允許 Plan 直接到 Execute
    assert ("Plan", "Execute") not in edges

def test_all_paths_end(workflow_mermaid):
    nodes, edges = parse_mermaid_states(workflow_mermaid)
    # 檢查所有終止節點都能到 [*]
    assert ("Verify", "[*]") in edges
    assert ("Error", "[*]") in edges