def gcd(a, b):
    '''
    Hàm tính ước chung lớn nhất (GCD) của hai số nguyên a và b.
    Sử dụng thuật toán Euclid.
    :param a: Số nguyên thứ nhất
    :param b: Số nguyên thứ hai
    :return: GCD của a và b
    '''
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    '''
    Hàm tính ước chung lớn nhất (GCD) của hai số nguyên a và b,
    đồng thời tìm hai số x, y sao cho ax + by = gcd(a, b).
    Sử dụng thuật toán Euclid mở rộng.

    Áp dụng thuật toán trong tìm hệ số d trong RSA.
    Thay a = e, b = phi(n), ta sẽ tìm được d sao cho ed ≡ 1 (mod phi(n)).

    :param a: Số nguyên thứ nhất
    :param b: Số nguyên thứ hai
    :return: Tuple (gcd, x, y) với gcd là ước chung lớn nhất của a và b,
                x và y là các số thỏa mãn ax + by = gcd(a, b)
    '''
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def is_prime(n):
    '''
    Hàm kiểm tra xem một số nguyên n có phải là số nguyên tố hay không.
    Một số nguyên tố là số lớn hơn 1 và chỉ chia hết cho 1 và chính nó.

    :param n: Số nguyên cần kiểm tra
    :return: True nếu n là số nguyên tố, False nếu không phải
    '''
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    r = is_prime(31)
    print(f"Is 31 prime? {r}")