# SnowCrash Level14 Walkthrough

## Objective:

Bypass the UID check in the Level14 executable to get the token for flag14.

## Step 1: Analyze the Directory

The directory is empty we have nothing:

This means that the only solution we have is to debug the binary file of /bin/getflag

## Step 2: Reverse Engineering (Decompilation)

Using [Dogbolt](https://dogbolt.org), we can see that the file contains a lot of ft_des, we can target the last one since we have 14 levels:

### Using GDB:

1. Disassemble main:

```bash
gdb /bin/getflag
(gdb) disassemble main
```

Output:

```bash
# output is large we target just the last ft_des
   0x08048de3 <+1181>:  jmp    0x8048e2f <main+1257>
   0x08048de5 <+1183>:  mov    0x804b060,%eax
   0x08048dea <+1188>:  mov    %eax,%ebx
   0x08048dec <+1190>:  movl   $0x8049220,(%esp)
   0x08048df3 <+1197>:  call   0x8048604 <ft_des>
   0x08048df8 <+1202>:  mov    %ebx,0x4(%esp)
  # .....
End of assembler dump.
```

2. Set a Breakpoint from top of the assembler dump:

```bash
(gdb) break *0x08048946
Breakpoint 1 at 0x8048946
```

3. Run the Program:

```bash
(gdb) run
Starting program: /bin/getflag

Breakpoint 1, 0x08048946 in main ()
```

4. Jump to section befor ft_des

```bash
(gdb) jump *0x08048de5
```

5. Get the Token:

```bash
Continuing at 0x8048de5.
7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
*** stack smashing detected ***: /bin/getflag terminated

Program received signal SIGSEGV, Segmentation fault.
0xb7e1c788 in ?? () from /lib/i386-linux-gnu/libgcc_s.so.1
```

## Next Steps

With the flag 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ, we can now proceed to flag14 of the SnowCrash challenge.

## Final step

```bash
level14@SnowCrash:~$ su flag14
Password:
Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)
flag14@SnowCrash:~$ getflag
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

Congratulations we managed to finish the project snowCrash
