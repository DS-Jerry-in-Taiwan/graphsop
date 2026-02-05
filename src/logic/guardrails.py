"""
Constraint Engine (Guardrails) for TwinLex Phase 03
- 檢查意圖是否違反物理極限或安全規範
- 查詢圖譜 Constraint 節點，支援多重約束
"""

from typing import Dict, Any, List

class ConstraintViolation(Exception):
    def __init__(self, reason: str, violated_constraint_id: str):
        self.reason = reason
        self.violated_constraint_id = violated_constraint_id
        super().__init__(reason)

def check_safety(intent: Dict[str, Any], constraints: List[Dict[str, Any]], current_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    檢查意圖是否合法，若違規則回傳詳細原因與違規約束ID
    """
    # 1. 物理限制檢查
    if "parameters" in intent:
        params = intent["parameters"]
        for c in constraints:
            if c.get("type") == "Max_Pan_Angle":
                max_pan = float(c.get("value", 180))
                if params.get("angle") and abs(params["angle"]) > max_pan:
                    return {
                        "allowed": False,
                        "reason": f"超過最大旋轉角度限制({max_pan}度)",
                        "violated_constraint_id": c.get("id", "unknown")
                    }
            if c.get("type") == "Zoom_Limit":
                max_zoom = float(c.get("value", 10))
                if params.get("zoom_level") and params["zoom_level"] > max_zoom:
                    return {
                        "allowed": False,
                        "reason": f"超過最大變焦倍率({max_zoom}x)",
                        "violated_constraint_id": c.get("id", "unknown")
                    }
    # 2. 區域限制檢查
    target_id = intent.get("target_id")
    for c in constraints:
        if c.get("type") in ["Privacy_Zone", "Restricted_Area"]:
            if target_id and target_id == c.get("target_id"):
                return {
                    "allowed": False,
                    "reason": f"目標區域為 {c.get('type')}，禁止操作",
                    "violated_constraint_id": c.get("id", "unknown")
                }
    # 3. 狀態衝突檢查
    if current_state.get("locked") and intent.get("action") == "ROTATE":
        return {
            "allowed": False,
            "reason": "設備未解鎖，禁止旋轉",
            "violated_constraint_id": "LOCKED"
        }
    # 通過所有檢查
    return {
        "allowed": True,
        "reason": "",
        "violated_constraint_id": None
    }