import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "logic")))
from guardrails import check_safety
from planner import plan_sop_steps

def test_full_workflow_success():
    # 合法指令：旋轉 90 度到大門
    intent = {"action": "ROTATE", "parameters": {"angle": 90}, "target_id": "door"}
    constraints = [{"type": "Max_Pan_Angle", "value": 180, "id": "C1"}]
    current_state = {"locked": False}
    graph_path = ["MOTOR_LOCK", "ROTATE"]
    # 1. 安全檢查
    safety = check_safety(intent, constraints, current_state)
    assert safety["allowed"]
    # 2. SOP 規劃
    steps = plan_sop_steps(intent, graph_path)
    assert steps[0]["action"] == "UNLOCK_MOTOR"
    assert steps[1]["action"] == "ROTATE"
    assert steps[1]["params"]["angle"] == 90

def test_full_workflow_violation():
    # 違規指令：旋轉 400 度
    intent = {"action": "ROTATE", "parameters": {"angle": 400}, "target_id": "door"}
    constraints = [{"type": "Max_Pan_Angle", "value": 180, "id": "C1"}]
    current_state = {"locked": False}
    graph_path = ["MOTOR_LOCK", "ROTATE"]
    # 1. 安全檢查
    safety = check_safety(intent, constraints, current_state)
    assert not safety["allowed"]
    assert "最大旋轉角度" in safety["reason"]
    # 2. SOP 不應執行
    if safety["allowed"]:
        steps = plan_sop_steps(intent, graph_path)
        assert False, "違規指令不應進入 SOP 規劃"

def test_full_workflow_privacy_zone():
    # 違規指令：目標為隱私區
    intent = {"action": "ROTATE", "parameters": {"angle": 90}, "target_id": "zone_b"}
    constraints = [{"type": "Privacy_Zone", "target_id": "zone_b", "id": "C3"}]
    current_state = {"locked": False}
    graph_path = ["MOTOR_LOCK", "ROTATE"]
    safety = check_safety(intent, constraints, current_state)
    assert not safety["allowed"]
    assert "Privacy_Zone" in safety["reason"]