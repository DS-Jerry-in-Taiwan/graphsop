from typing import List, Optional, Any
from pydantic import BaseModel, Field

class SOPStep(BaseModel):
    camera_name: str
    action: str
    sop_step: str

class MultiStepResult(BaseModel):
    output: str
    camera_name: str
    action: str
    sop_step: str
    error: Optional[str] = None

class AgentResponse(BaseModel):
    output: str
    can_auto_sop: Optional[bool] = None
    error: Optional[str] = None
    sop_steps: Optional[List[str]] = None
    sop_structured: Optional[List[SOPStep]] = None
    multi_step_result: Optional[List[MultiStepResult]] = None