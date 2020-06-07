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
