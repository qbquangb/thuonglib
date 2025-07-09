

def build_config(config, separator='.'):
    """
    Chuyển cấu trúc lồng nhau (dict, list, tuple) thành một flat dict.
    Mỗi key trong kết quả sẽ bắt đầu bằng separator, theo từng bước xuống sâu.

    Ví dụ:
    config = {'a': {'b': 1}, 'c': [2, 3]}
    build_config(config) =>
        {
        '.a': {'b': 1},
        '.a.b': 1,
        '.c': [2, 3],
        '.c.0': 2,
        '.c.1': 3
        }
    """
    flat_dict = {}

    # 1) Nếu là dict: đệ quy flatten từng giá trị, rồi ghi sub-keys với prefix là tên key hiện tại
    if isinstance(config, dict):
        for k, v in config.items():
            sub = build_config(v, separator)
            # merge các kết quả con (nếu có)
            if sub:
                for sub_key, sub_val in sub.items():
                    # sub_key đã bắt đầu bằng separator, nên nối: .k + sub_key
                    flat_dict[f"{separator}{k}{sub_key}"] = sub_val
            # bản thân node hiện tại cũng được lưu
            flat_dict[f"{separator}{k}"] = v

    # 2) Nếu là list hoặc tuple: tương tự, dùng index làm key
    elif isinstance(config, (list, tuple)):
        for idx, v in enumerate(config):
            sub = build_config(v, separator)
            if sub:
                for sub_key, sub_val in sub.items():
                    flat_dict[f"{separator}{idx}{sub_key}"] = sub_val
            flat_dict[f"{separator}{idx}"] = v

    # 3) Nếu là kiểu cơ bản (int, str, v.v.), không flatten tiếp
    else:
        # Trả về {} để biểu thị “không có dict con”
        return {}

    return flat_dict