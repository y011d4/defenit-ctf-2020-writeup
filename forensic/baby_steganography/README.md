## Baby Steganography

#### Description

```
I heared you can find hide data in Audio Sub Bit.
Do you want to look for it?
```

#### Writeup

配布物である `problem` ファイルをバイナリエディタで読むと、前半部分に `0x00`, `0x01` が並んでいる。8bytes ごとに区切って軽く手計算をしてみると、これらの値が ascii コードに対応していそう。なので、それらを読むコードを書いた。

```python
import wave
import struct

wav = wave.open("problem", mode="rb")
print(wav.getparams())

frame_bytes = bytearray(list(wav.readframes(wav.getnframes())))
print(frame_bytes[:100])

result = []
for i in range(100):
    buf = frame_bytes[i * 8 : (i + 1) * 8]
    buf = "".join([str(b) for b in buf])
    result.append(chr(int(buf, 2)))
print("".join(result))

wav.close()
```

`Defenit{Y0u_knOw_tH3_@uD10_5t39@No9rAphy?!}`