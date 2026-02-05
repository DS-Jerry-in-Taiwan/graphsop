import re
from typing import Dict, Any

def extract_slots(intent: str, user_input: str) -> Dict[str, Any]:
    """
    根據意圖與 user_input 動態抽取 slot（參數），並回傳缺少的欄位。
    """
    slots = {}
    missing = []
    camera_name = None
    action = None
    value = None

    # 攝影機名稱抽取
    m = re.search(r"(TwinLex\S*|camera\S*|攝影機\S*)", user_input)
    if m:
        camera_name = m.group(1)
    if not camera_name:
        missing.append("攝影機名稱")
    slots["camera_name"] = camera_name

    # 控制意圖下抽取動作與數值
    if intent == "CONTROL":
        if "旋轉" in user_input or "rotate" in user_input:
            action = "rotate"
            m = re.search(r"(\d+)", user_input)
            if m:
                value = float(m.group(1))
        if "變焦" in user_input or "zoom" in user_input:
            action = "zoom"
            m = re.search(r"(\d+)", user_input)
            if m:
                value = float(m.group(1))
        if not action:
            missing.append("動作")
        if value is None:
            missing.append("數值")
        slots["action"] = action
        slots["value"] = value

    return {"slots": slots, "missing": missing}