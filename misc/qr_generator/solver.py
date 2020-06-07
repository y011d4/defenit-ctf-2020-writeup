import numpy as np
from PIL import Image
from pwn import *
from pyzbar.pyzbar import decode

context.log_level = "DEBUG"
r = remote("qr-generator.ctf.defenit.kr", 9000)

r.sendlineafter("What is your Hero's name? ", "hoge")

for _ in range(100):
    r.recvuntil("< QR >\n")
    qr = r.recvuntil("\n\n")
    qr = np.array(qr.split()).astype(bool)
    qr = qr.reshape(int(np.sqrt(len(qr))), -1)
    qr = np.pad(qr, (1, 1), "constant")
    qr = 1 - qr
    print(qr)
    img = Image.fromarray(qr.astype(bool))
    data = decode(img)
    print(data[0].data)
    r.sendlineafter(">> ", data[0].data)
r.recvall()
