from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from src.schema.intents import ActionType, ControlParameters, ControlIntent

class ExtractorOutput(BaseModel):
    action: ActionType
    target_entity: Optional[str]
    parameters: Optional[ControlParameters]

def extract_parameters(user_input: str, graph_entities_context: Optional[Dict[str, Any]] = None) -> ExtractorOutput:
    """
    從 CONTROL 指令中提取 action、target_entity、parameters。
    實際應用可用 LLM 或規則引擎，這裡為簡化範例。
    """
    text = user_input.strip().lower()
    # 假設簡單關鍵字對應
    if "左" in text:
        direction = "LEFT"
    elif "右" in text:
        direction = "RIGHT"
    elif "上" in text:
        direction = "UP"
    elif "下" in text:
        direction = "DOWN"
    else:
        direction = None

    angle = None
    zoom_level = None
    import re
    angle_match = re.search(r"(\d+)\s*度", text)
    if angle_match:
        angle = float(angle_match.group(1))
    zoom_match = re.search(r"(\d+)\s*倍", text)
    if zoom_match:
        zoom_level = float(zoom_match.group(1))

    if "變焦" in text or "zoom" in text:
        action = ActionType.ZOOM
    elif "轉" in text or "旋轉" in text:
        action = ActionType.ROTATE
    elif "重設" in text or "reset" in text:
        action = ActionType.RESET
    else:
        action = ActionType.ROTATE

    # 假設 target_entity 直接取第一個出現的地點/設備名
    target_entity = None
    if graph_entities_context:
        for entity in graph_entities_context.get("entities", []):
            if entity["name"] in text:
                target_entity = entity["name"]
                break

    params = ControlParameters(angle=angle, direction=direction, zoom_level=zoom_level)
    return ExtractorOutput(action=action, target_entity=target_entity, parameters=params)