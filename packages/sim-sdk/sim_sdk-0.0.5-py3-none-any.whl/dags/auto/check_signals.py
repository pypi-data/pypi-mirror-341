# -*- coding: utf-8 -*-
def run_signal_checks(message, frame):
    """ 检查信号是否在范围内，并返回检查结果 """
    check_result = {
        "valid_signals": {},
        "invalid_signals": {}
    }

    for signal_name, value in message.items():
        signal = frame.get_signal_by_name(signal_name)
        if signal is None:
            continue

        min_value = signal.minimum
        max_value = signal.maximum

        if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
            check_result["invalid_signals"][signal_name] = {
                "value": value,
                "min": min_value,
                "max": max_value
            }
        else:
            check_result["valid_signals"][signal_name] = value

    return check_result
