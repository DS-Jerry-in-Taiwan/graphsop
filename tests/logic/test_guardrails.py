import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "logic")))
from guardrails import check_safety

def test_pan_angle_violation():
    intent = {"action": "ROTATE", "parameters": {"angle": 200}, "target_id": "zone_a"}
    constraints = [{"type": "Max_Pan_Angle", "value": 180, "id": "C1"}]
    current_state = {}
    result = check_safety(intent, constraints, current_state)
    assert not result["allowed"]
    assert "最大旋轉角度" in result["reason"]
    assert result["violated_constraint_id"] == "C1"

def test_zoom_limit_violation():
    intent = {"action": "ZOOM", "parameters": {"zoom_level": 20}, "target_id": "zone_a"}
    constraints = [{"type": "Zoom_Limit", "value": 10, "id": "C2"}]
    current_state = {}
    result = check_safety(intent, constraints, current_state)
    assert not result["allowed"]
    assert "最大變焦倍率" in result["reason"]
    assert result["violated_constraint_id"] == "C2"

def test_privacy_zone_violation():
    intent = {"action": "ROTATE", "parameters": {"angle": 90}, "target_id": "zone_b"}
    constraints = [{"type": "Privacy_Zone", "target_id": "zone_b", "id": "C3"}]
    current_state = {}
    result = check_safety(intent, constraints, current_state)
    assert not result["allowed"]
    assert "Privacy_Zone" in result["reason"]
    assert result["violated_constraint_id"] == "C3"

def test_locked_state_violation():
    intent = {"action": "ROTATE", "parameters": {"angle": 90}, "target_id": "zone_a"}
    constraints = []
    current_state = {"locked": True}
    result = check_safety(intent, constraints, current_state)
    assert not result["allowed"]
    assert "未解鎖" in result["reason"]
    assert result["violated_constraint_id"] == "LOCKED"

def test_all_pass():
    intent = {"action": "ROTATE", "parameters": {"angle": 90}, "target_id": "zone_a"}
    constraints = [{"type": "Max_Pan_Angle", "value": 180, "id": "C1"}]
    current_state = {"locked": False}
    result = check_safety(intent, constraints, current_state)
    assert result["allowed"]
    assert result["reason"] == ""
    assert result["violated_constraint_id"] is None