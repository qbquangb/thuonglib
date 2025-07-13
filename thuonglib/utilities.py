

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

def split_bytes(data: bytes, separator: bytes = b'*****') -> list[bytes]:
    """
    Tách dữ liệu bytes thành các đoạn con dựa trên separator.
    Trả về danh sách các đoạn bytes.

    Example:
        data = b'begin_file1-----data1-----end_file1*****begin_file2-----data2-----end_file2'
        split_bytes(data) => [b'data1', b'data2']
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be of type bytes")
    if not isinstance(separator, bytes):
        raise TypeError("separator must be of type bytes")
    segments = data.split(separator)
    datas = []
    for seg in segments:
        parts = seg.split(b'-----')
        # parts sẽ có dạng [b'begin_fileX', b'dataX', b'end_fileX']
        if len(parts) == 3:
            datas.append(parts[1])
    return datas

if __name__ == "__main__":
    b = "begin_file1-----data1-----end_file1*****begin_file2-----data2-----end_file2".encode('utf-8')

    r = split_bytes(b)
    print(r)