## QR Generator

#### Description

```
Escape from QR devil!
```

#### Writeup

0, 1 で QR コードを表した文字列が渡される (100個) ので、それをデコードして文字列を返す問題。スクリプトを書いた。

```python
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
```

(地味に0と1が思ったのと逆だったのと、QRコードの画像を生成したときに周囲に白背景を作らないとうまく読み取れないところにハマった)

`Defenit{QQu!_3sC4p3_FR0m_D3v1l!_n1c3_C0gN1z3!}`

