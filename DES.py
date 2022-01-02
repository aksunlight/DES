#python3.10下编译通过
#工作模式：ECB  填充模式：no padding
#加密：输入：UTF-8字符    输出：Base64字符
#解密：输入：Base64字符    输出：UTF-8字符
import os
import base64
import bitstring


IP_table = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

IP_re_table = [40, 8, 48, 16, 56, 24, 64, 32,
               39, 7, 47, 15, 55, 23, 63, 31,
               38, 6, 46, 14, 54, 22, 62, 30,
               37, 5, 45, 13, 53, 21, 61, 29,
               36, 4, 44, 12, 52, 20, 60, 28,
               35, 3, 43, 11, 51, 19, 59, 27,
               34, 2, 42, 10, 50, 18, 58, 26,
               33, 1, 41, 9, 49, 17, 57, 25]
      
PC_1 = [57, 49, 41, 33, 25, 17,9,
       1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27,
      19, 11,  3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29,
      21, 13,  5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24,  1,  5,
         3, 28, 15,  6, 21, 10,
        23, 19, 12,  4, 26,  8,
        16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

E  = [32, 1,  2,  3,  4,  5,
      4,  5,  6,  7,  8,  9,
      8,  9,  10, 11, 12, 13,
      12, 13, 14, 15, 16, 17,
      16, 17, 18, 19, 20, 21,
      20, 21, 22, 23, 24, 25,
      24, 25, 26, 27, 28, 29,
      28, 29, 30, 31, 32,  1]

S = [
    [[14, 4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
     [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
     [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10, 0,  6, 13]],

    [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12, 0,  5, 10],
     [3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
     [0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
     [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14, 9]],

    [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
     [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
     [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
     [1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],

    [[7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11,  12,  4, 15],
     [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
     [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
     [3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],

    [[2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
     [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3, 9,  8,  6],
     [4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
     [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5, 3]],

    [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
     [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3, 8],
     [9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
     [4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],

    [[4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
     [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8, 6],
     [1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
     [6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],

    [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12, 7],
     [1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
     [7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
     [2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]],
]

P = [16,  7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
     32, 27, 3,  9,
     19, 13, 30, 6,
     22, 11, 4, 25]


#密钥初始化
def init_key(origin_key):
    res = bitstring.BitStream(uint=0, length=56)
    for i in range(56):
        res[i] = origin_key[PC_1[i] - 1]
    return res

#生成子密钥
def sub_key(init_key):
    sub_key = []
    for i in range(16):
        lk = init_key[0:28]; lk.rol(SHIFT[i])
        rk = init_key[28:56]; rk.rol(SHIFT[i])
        init_key = lk + rk
        res = bitstring.BitStream(uint=0, length=48)
        for j in range(48):
            res[j] = init_key[PC_2[j] - 1]
        sub_key.append(res)
    return sub_key

#初始置换
def init(origin_str):
    res = bitstring.BitStream(uint=0, length=64)
    for i in range(64):
        res[i] = origin_str[IP_table[i] - 1]
    return res

#扩展置换
def extend(init_str):
    res = bitstring.BitStream(uint=0, length=48)
    for i in range(48):
        res[i] = init_str[E[i] - 1]
    return res

#S盒置换
def sbox(bstr):
    idx = 0; res = bitstring.BitStream()
    for i in range(8):
        sx = bstr[idx:idx+6]
        row = sx[::5]; col = sx[1:5]
        x = row.uint; y = col.uint
        res = res + bitstring.BitStream(uint=S[i][x][y], length=4)
        idx = idx + 6
    return res

#直接置换
def direct(bstr):
    res = bitstring.BitStream(uint=0, length=32)
    for i in range(32):
        res[i] = bstr[P[i] - 1]
    return res

#16轮循环（加密）
def ploop(init_str, sub_key):
    ls = init_str[0:32]; rs = init_str[32:64]
    for i in range(16):
        next_rs = extend(rs) ^ sub_key[i]
        next_rs = sbox(next_rs)
        next_rs = direct(next_rs)
        next_rs = next_rs ^ ls
        ls = rs; rs = next_rs
    return rs + ls

#16轮循环（解密）
def nloop(init_str, sub_key):
    ls = init_str[0:32]; rs = init_str[32:64]
    for i in range(15, -1, -1):
        next_rs = extend(rs) ^ sub_key[i]
        next_rs = sbox(next_rs)
        next_rs = direct(next_rs)
        next_rs = next_rs ^ ls
        ls = rs; rs = next_rs
    return rs + ls

#终结置换
def final(bstr):
    res = bitstring.BitStream(uint=0, length=64)
    for i in range(64):
        res[i] = bstr[IP_re_table[i] - 1]
    return res

#DES加密
def encryption(plaintext, key):
    idx = 0; res = bytes()
    a = bitstring.BitStream(plaintext)
    while idx < len(plaintext) * 8:
        gp = a[idx:idx+64]
        counts = len(gp)
        if (counts < 64):
            gp = gp + bitstring.BitStream(uint=0, length=64-counts)
        res = res + final(ploop(init(gp), sub_key(init_key(key)))).bytes
        idx = idx + 64
    return res

#DES解密
def decrypt(ciphertext, key):
    idx = 0; res = bytes()
    a = bitstring.BitStream(ciphertext)
    while idx < len(ciphertext) * 8:
        gp = a[idx:idx+64]
        counts = len(gp)
        if (counts < 64):
            gp = gp + bitstring.BitStream(uint=0, length=64-counts)
        res = res + final(nloop(init(gp), sub_key(init_key(key)))).bytes
        idx = idx + 64
    return res


#DES加密(密文用Base64编码)
with open('./明文.txt', 'r', encoding='utf-8') as fp1, open('./密文.txt', 'a', encoding='utf-8') as fp2:
    #将文件中的数据按行进行加密
    key = bitstring.BitStream(bytes(input('请输入8个字符长度的DES密钥：'), 'ascii'))
    for line in fp1:
        line = line.strip()     #用来删除头尾空白符：\r \n \t ' '
        if (line == ''):
            continue
        plaintext = line.encode('utf-8')
        ciphertext = encryption(plaintext, key)
        ciphertext_base64 = base64.b64encode(ciphertext)
        readciphertext_base64 = ciphertext_base64.decode('utf-8')
        fp2.write(readciphertext_base64 + '\n')
        print('明文：', line, '对应的密文为：', readciphertext_base64)

#DES解密(密文用Base64编码)
with open('./密文.txt', 'r', encoding='utf-8') as fp1, open('./解密.txt', 'a', encoding='utf-8') as fp2:
    #将文件中的数据按行进行解密
    key = bitstring.BitStream(bytes(input('请输入8个字符长度的DES密钥：'), 'ascii'))
    for line in fp1:
        line = line.strip()     #用来删除头尾空白符：\r \n \t ' '
        if (line == ''):
            continue
        ciphertext = base64.b64decode(line)
        plaintext = decrypt(ciphertext, key)
        readplaintext = plaintext.decode('utf-8').rstrip(b'\x00'.decode('utf-8'))
        fp2.write(readplaintext + '\n')
        print('密文：', line, '对应的明文为：', readplaintext)

os.system('pause')
