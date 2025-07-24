from Crypto.Hash import SHA256, SHA512, SHA3_256, SHA3_512
from thuonglib.utilities import cipher_utilities

def my_hash(data: bytes | str = None, file_write = 0) -> str:
    """
    Tạo giá trị băm SHA-256 từ dữ liệu đầu vào.
    Nếu dữ liệu là chuỗi, nó sẽ được mã hóa utf-8 trước khi băm.
    Nếu data = None, phải nhập đường dẫn đến file cần băm.

    :param data: Dữ liệu đầu vào (bytes hoặc str hoặc None)
    :return: Giá trị băm SHA-256 dưới dạng chuỗi hex, chứa 64 ký tự hex (32 bytes).
    """
    if data is None or data == '':
        input_file = r"{}".format(input("Nhập đường dẫn file cần hash: "))
        with open(input_file, 'rb') as file:
            data = file.read()
        hash_value = cipher_utilities.SHA_256(data)
        print("**********************************************************************")
        print(f"Giá trị băm SHA-256 của file {input_file} là: {hash_value}")
        print("**********************************************************************")
        if file_write:
            output_file = input_file + ".sha256"
            with open(output_file, 'w') as f:
                f.write(hash_value)
            print(f"Giá trị băm đã được lưu vào {output_file}")
        return hash_value
    else:
        hash_value = cipher_utilities.SHA_256(data)
        print("**********************************************************************")
        print(f"Giá trị băm SHA-256 của dữ liệu được tạo với hàm my_hash() là: {hash_value}")
        print("**********************************************************************")
        if 0:
            output_file = r"{}".format(input("Nhập đường dẫn file cần lưu giá trị băm: "))
            file_name = r'{}'.format(input("Nhập tên file lưu giá trị băm (không cần đuôi): "))
            output_file += file_name + ".sha256"
            with open(output_file, 'w') as f:
                f.write(hash_value)
            print(f"Giá trị băm đã được lưu vào {output_file}")
        return hash_value
    
def sha256(data: bytes | str = None, file_write = 1) -> str:
    """
    Tạo giá trị băm SHA-256 từ dữ liệu đầu vào.
    Nếu dữ liệu là chuỗi, nó sẽ được mã hóa utf-8 trước khi băm.
    Nếu data = None, phải nhập đường dẫn đến file cần băm.
    
    :param data: Dữ liệu đầu vào (bytes hoặc str hoặc None)
    :return: Giá trị băm SHA-256 dưới dạng chuỗi hex, chứa 64 ký tự hex (32 bytes).
    """
    if data is None or data == '':
        input_file = r"{}".format(input("Nhập đường dẫn file cần hash: "))
        with open(input_file, 'rb') as file:
            data = file.read()
        sha256_hash = SHA256.new()
        sha256_hash.update(data)
        sha256_digest = sha256_hash.hexdigest()
        print("**********************************************************************")
        print(f"Giá trị băm SHA-256 của file {input_file} là: {sha256_digest}")
        print("**********************************************************************")
        # print(f"giá trị hash được tạo từ hàm my_hash() và sha256() là {'bằng nhau' if sha256_digest == my_hash(data, file_write) else 'khác nhau'}")
        if file_write:
            output_file = input_file + ".sha256"
            with open(output_file, 'w') as f:
                f.write(sha256_digest)
            print(f"Giá trị băm đã được lưu vào {output_file}")
        return sha256_digest
    else:
        # Nếu data là chuỗi, mã hóa nó thành bytes
        sha256_hash = SHA256.new()
        sha256_hash.update(data.encode('utf-8') if isinstance(data, str) else data)
        sha256_digest = sha256_hash.hexdigest()
        print("**********************************************************************")
        print(f"Giá trị băm SHA-256 của data là: {sha256_digest}")
        print("**********************************************************************")
        print(f"giá trị hash được tạo từ hàm my_hash() và sha256() là {'bằng nhau' if sha256_digest == my_hash(data, file_write) else 'khác nhau'}")
        return sha256_digest

def main():
    # Dữ liệu đầu vào (chuỗi byte)
    data = b"Hello, World!"
    
    # Tạo giá trị băm SHA-256
    sha256_hash = SHA256.new()
    sha256_hash.update(data)
    sha256_digest = sha256_hash.hexdigest()
    
    # Tạo giá trị băm SHA-512
    sha512_hash = SHA512.new()
    sha512_hash.update(data)
    sha512_digest = sha512_hash.hexdigest()
    
    # Tạo giá trị băm SHA3-256
    sha3_256_hash = SHA3_256.new()
    sha3_256_hash.update(data)
    sha3_256_digest = sha3_256_hash.hexdigest()
    
    # Tạo giá trị băm SHA3-512
    sha3_512_hash = SHA3_512.new()
    sha3_512_hash.update(data)
    sha3_512_digest = sha3_512_hash.hexdigest()
    
    # In ra kết quả
    print("SHA-256:", sha256_digest)
    print("SHA-512:", sha512_digest)
    print("SHA3-256:", sha3_256_digest)
    print("SHA3-512:", sha3_512_digest)

if __name__ == "__main__":
    import sys
    sys.path.pop(0)

    data = 'Hello, World!'
    my_hash(data, file_write=1)