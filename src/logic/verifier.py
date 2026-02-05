class VerificationError(Exception):
    pass

def verify_execution(expected_state, actual_state, tolerance=0.05):
    """
    比對 expected_state (SOP 預期) 與 actual_state (Mock Device 回報)。
    容許 5% 數值誤差，超出則拋出 VerificationError。
    """
    for key, expected in expected_state.items():
        if key not in actual_state:
            raise VerificationError(f"缺少狀態欄位: {key}")
        actual = actual_state[key]
        # 僅比對數值型欄位
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            if expected == 0:
                if abs(actual) > tolerance:
                    raise VerificationError(f"{key} 偏差過大: {actual} (預期 0)")
            else:
                if abs(actual - expected) / abs(expected) > tolerance:
                    raise VerificationError(f"{key} 偏差超過容差: {actual} (預期 {expected})")
        else:
            if actual != expected:
                raise VerificationError(f"{key} 不符: {actual} (預期 {expected})")
    return True