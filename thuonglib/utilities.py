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

class cipher_utilities:

    @staticmethod
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
        from thuonglib.math_lib import gf_mul
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

    @staticmethod
    def rotr(x, n, w=32):
        '''
        Rotate right x by n bits in a w-bit word.
        x: integer to rotate
        n: number of bits to rotate
        w: word size in bits (default 32)
        Returns: rotated integer.

        Example usage:
        x = 0x12345678
        n = 4
        rotated = rotr(x, n)
        hex_rotated = f"{rotated:08x}"
        print(f"Rotated: {hex_rotated}")
        Output: Rotated: 81234567
        '''
        return ((x >> n) | (x << (w-n))) & (2**w-1)
    
    @staticmethod
    def sigma0(x):
        '''
        Compute the SHA-256 sigma0 function.
        x: 32-bit integer input
        Returns: 32-bit integer result of sigma0.

        Example usage:
        x = 0x12345678
        result = sigma0(x)
        hex_result = f"{result:08x}"
        print(f"Sigma0: {hex_result}")
        '''
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

    @staticmethod
    def sigma1(x):
        '''
        Compute the SHA-256 sigma1 function.
        x: 32-bit integer input
        Returns: 32-bit integer result of sigma1.

        Example usage:
        x = 0x12345678
        result = sigma1(x)
        hex_result = f"{result:08x}"
        print(f"Sigma1: {hex_result}")
        '''
        return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
    
    @staticmethod
    def SHA_256(message: bytes | str) -> str:
        import struct

        # Hằng số ban đầu (8 giá trị băm ban đầu - lấy từ căn bậc hai của các số nguyên tố đầu tiên)
        H = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]

        # Hằng số K cho 64 vòng lặp (lấy từ căn bậc ba của các số nguyên tố đầu tiên)
        K = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        def right_rotate(x, n):
            """Hàm xoay phải n bit trên số 32-bit."""
            return (x >> n) | (x << (32 - n)) & 0xFFFFFFFF

        def prepare_message(message):
            """Chuẩn bị dữ liệu đầu vào theo đặc tả SHA-256."""
            # Chuyển chuỗi thành bytes nếu chưa phải bytes
            if isinstance(message, str):
                message = message.encode()
            
            # Độ dài ban đầu của message (tính bằng bit)
            original_bit_len = len(message) * 8
            
            # Thêm bit '1' (byte 0x80)
            message += b'\x80'
            
            # Thêm các bit '0' để độ dài là bội số của 512, trừ 64 bit cuối
            while (len(message) * 8 + 64) % 512 != 0:
                message += b'\x00'
            
            # Thêm độ dài ban đầu dưới dạng số 64-bit (big-endian)
            message += struct.pack('>Q', original_bit_len)
            
            return message

        def sha256(message):
            """Hàm chính tính giá trị băm SHA-256."""
            # Chuẩn bị dữ liệu
            padded_message = prepare_message(message)
            
            # Khởi tạo các giá trị băm ban đầu
            h0, h1, h2, h3, h4, h5, h6, h7 = H
            
            # Chia dữ liệu thành các khối 512-bit
            for i in range(0, len(padded_message), 64):
                block = padded_message[i:i+64]
                
                # Mở rộng khối thành 64 từ 32-bit
                w = [0] * 64
                for j in range(16):
                    w[j] = struct.unpack('>I', block[j*4:j*4+4])[0]
                for j in range(16, 64):
                    s0 = right_rotate(w[j-15], 7) ^ right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
                    s1 = right_rotate(w[j-2], 17) ^ right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
                    w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF
                
                # Khởi tạo các biến cho vòng lặp
                a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
                
                # 64 vòng lặp chính
                for j in range(64):
                    S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
                    ch = (e & f) ^ ((~e) & g)
                    temp1 = (h + S1 + ch + K[j] + w[j]) & 0xFFFFFFFF
                    S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
                    maj = (a & b) ^ (a & c) ^ (b & c)
                    temp2 = (S0 + maj) & 0xFFFFFFFF
                    
                    h = g
                    g = f
                    f = e
                    e = (d + temp1) & 0xFFFFFFFF
                    d = c
                    c = b
                    b = a
                    a = (temp1 + temp2) & 0xFFFFFFFF
                
                # Cập nhật giá trị băm
                h0 = (h0 + a) & 0xFFFFFFFF
                h1 = (h1 + b) & 0xFFFFFFFF
                h2 = (h2 + c) & 0xFFFFFFFF
                h3 = (h3 + d) & 0xFFFFFFFF
                h4 = (h4 + e) & 0xFFFFFFFF
                h5 = (h5 + f) & 0xFFFFFFFF
                h6 = (h6 + g) & 0xFFFFFFFF
                h7 = (h7 + h) & 0xFFFFFFFF
            
            # Tạo giá trị băm cuối cùng dưới dạng chuỗi hex
            return ''.join(format(x, '08x') for x in [h0, h1, h2, h3, h4, h5, h6, h7])
        
        # Gọi hàm tính SHA-256
        return sha256(message)

if __name__ == "__main__":
    import sys
    sys.path.pop(0)

    message = "Hello, world!"
    hash_value = cipher_utilities.SHA_256(message)
    print(f"SHA-256 hash: {hash_value}")