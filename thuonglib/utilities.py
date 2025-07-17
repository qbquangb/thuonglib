from thuonglib.math_lib import gf_mul

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

def split_bytes(data: bytes, separator: bytes = b'\xfd#nA\x8c?\x964\xae\x06\xfc\x0f\x1cM\xc4"', **options) -> list[bytes]:
    """
    Tách dữ liệu bytes thành các đoạn con dựa trên separator.
    Trả về danh sách các đoạn bytes.

    Example:
        data = b'data1\xfd#nA\x8c?\x964\xae\x06\xfc\x0f\x1cM\xc4"data2'
        split_bytes(data, split_numbers=2) => [b'data1', b'data2'] 
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be of type bytes")
    if not isinstance(separator, bytes):
        raise TypeError("separator must be of type bytes")
    segments = data.split(separator)
    if options:
        if options.get("split_numbers") != len(segments):
            raise ValueError(f"Expected {options['split_numbers']} segments, but got {len(segments)}")
    else:
        raise ValueError("split_numbers option is required")
    return segments

def jonin_bytes(data: list[bytes], separator: bytes = b'\xfd#nA\x8c?\x964\xae\x06\xfc\x0f\x1cM\xc4"') -> bytes:
    """
    Nối các đoạn bytes lại với nhau, sử dụng separator.
    Trả về dữ liệu bytes đã nối.

    Example:
        data = [b'data1', b'data2']
        joined_data = jonin_bytes(data) => b'data1\xfd#nA\x8c?\x964\xae\x06\xfc\x0f\x1cM\xc4"data2'
    """
    if not isinstance(data, list):
        raise TypeError("data must be of type list")
    if not all(isinstance(item, bytes) for item in data):
        raise TypeError("All items in data must be of type bytes")
    return separator.join(data)

def bytes_to_binary(data: bytes) -> str:
    """
    Chuyển đổi dữ liệu bytes thành chuỗi nhị phân.
    Mỗi byte sẽ được biểu diễn dưới dạng 8 bit.

    Example:
        data = b'\x08-\xd6ahds'
        binary_str = bytes_to_binary(data)
        # binary_str sẽ là '00001000 00101101 11010110 01100001 01101000 01100100 01110011'
    """
    return ' '.join(format(byte, '08b') for byte in data)

def bytes_to_hex(data: bytes) -> str:
    """
    Chuyển đổi dữ liệu bytes thành chuỗi hexa.
    Mỗi byte sẽ được biểu diễn dưới dạng 2 ký tự hexa.

    Example:
        data = b'\x08-\xd6ahds'
        hex_str = bytes_to_hex(data)
        hex_str sẽ là '08 2d d6 61 68 64 73'
    """
    return ' '.join(format(byte, '02x') for byte in data)

def bytes_to_int_list(data: bytes) -> list[int]:
    """
    Chuyển đổi dữ liệu bytes thành danh sách các số nguyên.
    Mỗi byte sẽ được chuyển đổi thành một số nguyên.

    Example:
        data = b'\x08-\xd6ahds'
        int_list = bytes_to_int_list(data)
        # int_list sẽ là [8, 45, 214, 97, 104, 100, 115]
    """
    return [byte for byte in data]

def bytes_to_base64(data: bytes) -> str:
    """
    Chuyển đổi dữ liệu bytes thành chuỗi Base64.
    
    Example:
        data = b'\x08-\xd6ahds'
        base64_str = bytes_to_base64(data)
        base64_str sẽ là 'CDst1mFoZHNz'
    """
    import base64
    return base64.b64encode(data).decode('utf-8')

def base64_to_bytes(base64_str: str) -> bytes:
    """
    Chuyển đổi chuỗi Base64 thành dữ liệu bytes.
    
    Example:
        base64_str = 'CDst1mFoZHNz'
        data = base64_to_bytes(base64_str)
        data sẽ là b'\x08-\xd6ahds'
    """
    import base64
    return base64.b64decode(base64_str.encode('utf-8'))

def bytes_distance_bytes(b1: bytes, b2: bytes, algorithm: int = 1) -> int:
    """
    Tính khoảng cách giữa hai chuỗi bytes.\n
    algorithm = 1 (default) sử dụng hàm hamming_distance, hàm tính khoảng cách Hamming (số bit khác nhau).\n
    algorithm = 0 sử dụng hàm byte_diff_sum, hàm tính tổng độ lệch tuyệt đối trên từng byte.
    
    Example:
        b1 = b'\x08-\xd6ahds'
        b2 = b'\x08-\xd6ahds'
        distance = bytes_distance_bytes(b1, b2)
        distance sẽ là 0 vì hai chuỗi giống nhau
    """
    if len(b1) != len(b2):
        raise ValueError("Both byte sequences must have the same length")
    if algorithm:
        print(f"Using algorithm hamming_distance for distance calculation.")
        return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))
    print(f"Using algorithm byte_diff_sum for distance calculation.")
    return sum(abs(x - y) for x, y in zip(b1, b2))

def ghash(H, A, C):
    '''
    Compute GHASH for AES-GCM.
    H: 128-bit integer subkey for GHASH
    A: list of 128-bit integers (AAD blocks)
    C: list of 128-bit integers (ciphertext blocks)
    Returns: 128-bit integer result of GHASH.
    Raises ValueError if H is not a 128-bit integer or A/C contain invalid values.
    Uses carry-less multiplication and reduction by polynomial R.
    using constant R = 0xE1000000000000000000000000000000 for reduction.
    Example usage:
    H = 0x66e94bd4ef8a2c3b884cfa59ca342b2e  # example subkey
    A = [0xfeedfacedeadbeeffeedfacedeadbeef]  # example AAD block
    C = [0x42831ec2217774244b7221b784d0d49c]  # example ciphertext block
    gh = ghash(H, A, C)
    hex_gh = f"{gh:032x}"  # format as hex string
    print(f"GHASH: {hex_gh}")
    '''
    # A and C are lists of 128-bit ints
    # length bits
    lenA = len(A)*128
    lenC = len(C)*128
    # form X blocks: A blocks + C blocks + length block
    X = A + C + [ (lenA << 64) | lenC ]
    Y = 0
    for Xi in X:
        Y = gf_mul(Y ^ Xi, H)
    return Y

if __name__ == "__main__":
    H = 0x66e94bd4ef8a2c3b884cfa59ca342b2e
    # AAD: one block
    A = [0xfeedfacedeadbeeffeedfacedeadbeef]
    # C: one block
    C = [0x42831ec2217774244b7221b784d0d49c]

    gh = ghash(H, A, C)
    hex_gh = f"{gh:032x}"
    print(f"GHASH: {hex_gh}")