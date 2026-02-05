import streamlit as st
import time
import sys
import os

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.hardware.mock_camera import MockCamera
from src.logic.verifier import verify_execution, VerificationError
from src.agent.graph_agent import agent_executor

st.set_page_config(page_title="TwinLex 控制台", layout="wide")

# 初始化 MockCamera
if "camera" not in st.session_state:
    st.session_state["camera"] = MockCamera()

camera = st.session_state["camera"]

# 直接使用 agent_executor 統一入口
agent = agent_executor
    

st.sidebar.header("Mock Camera 狀態")
status_placeholder = st.sidebar.empty()

def update_status():
    status = camera.get_status()
    status_placeholder.json(status)

update_status()

st.title("TwinLex 智慧攝影機控制台")
st.write("請在下方輸入指令（如：旋轉到 30 度，變焦 5 倍）")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("輸入指令", key="user_input")
send = st.button("送出")

from src.nlu.router import classify_intent
from src.nlu.entity_resolver import extract_slots

if send and user_input:
    # --- Think 階段：NLU 統一分流與 slot filling ---
    intent_obj = classify_intent(user_input)
    intent = intent_obj.category.value if hasattr(intent_obj.category, "value") else str(intent_obj.category)
    slot_result = extract_slots(intent, user_input)
    missing = slot_result["missing"]
    slots = slot_result["slots"]
    camera_name = slots.get("camera_name")
    action = slots.get("action")
    value = slots.get("value")
    if missing:
        with st.chat_message("ai"):
            st.warning(f"請補齊必要資訊：{', '.join(missing)}")
        st.session_state["history"].append((user_input, [], "", f"缺少：{', '.join(missing)}", {}))
    else:
        # --- Action 階段 ---
        sop_steps = []
        result_msg = ""
        error_msg = ""
        if agent is None:
            st.error("GraphRAGAgent 未初始化，無法處理指令。")
            st.stop()
        else:
            agent_response = agent.invoke({"input": user_input})
            with st.chat_message("ai"):
                main_reply = agent_response.get("output") or agent_response.get("llm_reply", "")
                st.write(main_reply)
                # 若 agent_response 支援自動執行 SOP，顯示確認按鈕
                st.write(agent_response.get("can_auto_sop"))
                st.write(isinstance(agent_response, dict))
                st.write(agent_response)
                if agent_response.get("can_auto_sop"):
                    import json
                    if st.button("一鍵完成 SOP", key="auto_sop"):
                        sop_structured = agent_response.get("sop_structured", [])
                        exec_results = []
                        print("DEBUG SOP 結構化內容：", sop_structured)
                        if sop_structured:
                            print("DEBUG UI 傳給 agent 的 input:", json.dumps(sop_structured))
                            agent_result = agent.invoke({"input": json.dumps(sop_structured)})
                            multi_step_result = agent_result.get("multi_step_result", agent_result)
                            for i, step in enumerate(sop_structured):
                                desc = f"{step['camera_name']} 執行 {step['action']} 前需完成 {step['sop_step']}"
                                result = multi_step_result[i] if isinstance(multi_step_result, list) else multi_step_result
                                exec_results.append(f"已執行：{desc} → {result}")
                            st.success("所有 SOP 步驟已自動完成：\n" + "\n".join(exec_results))
                        else:
                            st.warning("未取得 SOP 結構化步驟，請檢查 agent 回傳格式。")
                if agent_response.get("error"):
                    st.error(f"Agent 查詢錯誤：{agent_response['error']}")
                with st.expander("GraphRAG Agent 回應細節"):
                    st.json(agent_response)
            if agent_response.get("can_execute"):
                if action == "rotate" and value is not None:
                    sop_steps.append({"action": "ROTATE", "params": {"pan": value, "tilt": 0}})
                    exec_result = camera.rotate(value, 0)
                    sop_steps[-1]["result"] = exec_result
                    try:
                        verify_execution({"pan": value}, camera.get_status())
                        result_msg = f"旋轉成功，目標角度 {value}°"
                    except VerificationError as e:
                        error_msg = f"驗證失敗：{e}"
                if action == "zoom" and value is not None:
                    sop_steps.append({"action": "ZOOM", "params": {"zoom": value}})
                    exec_result = camera.zoom(value)
                    sop_steps[-1]["result"] = exec_result
                    try:
                        verify_execution({"zoom": value}, camera.get_status())
                        result_msg = f"變焦成功，目標倍率 {value}x"
                    except VerificationError as e:
                        error_msg = f"驗證失敗：{e}"
                update_status()
                with st.chat_message("ai"):
                    if result_msg:
                        st.success(result_msg)
                    if error_msg:
                        st.error(error_msg)
                    with st.expander("SOP 步驟與執行結果"):
                        st.json(sop_steps)
            st.session_state["history"].append((user_input, sop_steps, result_msg, error_msg, agent_response))

# 自動刷新側邊欄狀態
st_autorefresh = st.sidebar.button("手動刷新狀態")
if st_autorefresh:
    update_status()