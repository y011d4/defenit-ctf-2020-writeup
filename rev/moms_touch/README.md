## MoM's Touch

#### Description

```
My mom wants me to bring a flag..
Please get my flag back to me!
```

#### Writeup

アセンブリが理解できなかったので力技で解いた。radare2 で解析したところ、以下の関数部分で入力文字列 (=フラグ) が正しいかを判定している。

```
    ; assembly                                           | /* r2dec pseudo code output */
                                                         | /* momsTouch @ 0x80487a1 */
                                                         | #include <stdint.h>
                                                         |
    ; (fcn) fcn.080487a0 ()                              | int32_t fcn_080487a0 (int32_t arg_4h) {
    0x080487a0 push ebp                                  |
    0x080487a1 push ebx                                  |
    0x080487a2 push edi                                  |
    0x080487a3 push esi                                  |
    0x080487a4 sub esp, 0xc                              |
    0x080487a7 xor esi, esi                              |     esi = 0;
    0x080487a9 mov edi, dword [esp + 0x20]               |     edi = arg_4h;
    0x080487ad mov ebx, 0x80808081                       |     ebx = 0x80808081;
    0x080487b2 nop word cs:[eax + eax]                   |
                                                         |     do {
    0x080487c0 mov eax, dword [esi*4 + 0x80492ac]        |         eax = *((esi*4 + 0x80492ac));
    0x080487c7 mov ecx, eax                              |         ecx = *((esi*4 + 0x80492ac));
    0x080487c9 shl ecx, 4                                |         ecx <<= 4;
    0x080487cc shr eax, 4                                |         eax >>= 4;
    0x080487cf or eax, ecx                               |         eax |= ecx;
    0x080487d1 movzx ebp, al                             |         ebp = (int32_t) al;
    0x080487d4 call 0x8048570                            |         eax = rand ();
    0x080487d9 mov ecx, eax                              |         ecx = eax;
    0x080487db imul ebx                                  |         edx:eax = eax * ebx;
    0x080487dd add edx, ecx                              |         edx += ecx;
    0x080487df mov eax, edx                              |         eax = edx;
    0x080487e1 shr eax, 0x1f                             |         eax >>= 0x1f;
    0x080487e4 sar edx, 7                                |         edx >>= 7;
    0x080487e7 add edx, eax                              |         edx += eax;
    0x080487e9 imul eax, edx, 0xff                       |         eax = edx * 0xff;
    0x080487ef sub ecx, eax                              |         ecx -= eax;
    0x080487f1 lea eax, [ecx*4]                          |         eax = ecx*4;
    0x080487f8 shr ecx, 2                                |         ecx >>= 2;
    0x080487fb or ecx, eax                               |         ecx |= eax;
    0x080487fd movzx eax, cl                             |         eax = (int32_t) cl;
    0x08048800 movsx ecx, byte [edi + esi]               |         ecx = *((edi + esi));
    0x08048804 xor ecx, dword [ebp*4 + 0x80492ac]        |         ecx ^= *((ebp*4 + 0x80492ac));
    0x0804880b xor ecx, dword [eax*4 + 0x80492ac]        |         ecx ^= *((eax*4 + 0x80492ac));
    0x08048812 cmp ecx, dword [esi*4 + 0x8049144]        |
                                                         |         if (ecx != *((esi*4 + 0x8049144))) {
    0x08048819 jne 0x8048825                             |             goto label_0;
                                                         |         }
    0x0804881b inc esi                                   |         esi++;
    0x0804881c mov al, 1                                 |         al = 1;
    0x0804881e cmp esi, 0x48                             |
    0x08048821 jle 0x80487c0                             |
                                                         |     } while (esi <= 0x48);
    0x08048823 jmp 0x8048827                             |     goto label_1;
                                                         | label_0:
    0x08048825 xor eax, eax                              |     eax = 0;
                                                         | label_1:
    0x08048827 movzx eax, al                             |     eax = (int32_t) al;
    0x0804882a add esp, 0xc                              |
    0x0804882d pop esi                                   |
    0x0804882e pop edi                                   |
    0x0804882f pop ebx                                   |
    0x08048830 pop ebp                                   |
    0x08048831 ret                                       |     return eax;
                                                         | }
```

`0x080487d4` 以下でやられている計算が何に該当するのかがわからなかったのと、 rand が返す値を検証するのが面倒だったため、プログラムを実行して gdb をアタッチし、`0x80492ac`や `0x8049144` に何の値が格納されているかをメモ。また、for loop 中に `0x08048812` にブレークポイントをはって、そのときの `eax` の値をメモした。プログラムに入力したフラグは当然適当なためブレークポイント後に普通に実行すると `0x08048819` で for loop から抜けてしまうため、 `eip` の値をいじることで if 文の分岐を無視した。

`eax` , `ebp` の値と `0x80492ac`や `0x8049144` あたりの値の xor を計算することで、フラグが求まる。

```python
result = []
for i in range(73):
    ebp = (memory[i] >> 4) | (memory[i] << 4)
    ebp %= 256
    eax = rand[i]
    result.append(chr(memory[eax] ^ memory[ebp] ^ data[i]))
print("".join(result))
```

`Defenit{ea40d42bfaf7d1f599abf284a35c535c607ccadbff38f7c39d6d57e238c4425e}`