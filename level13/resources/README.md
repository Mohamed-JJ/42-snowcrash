# SnowCrash Level13 Walkthrough

## Objective:

Bypass the UID check in the level13 executable to get the token for flag14.

## Step 1: Analyze the Binary

When we run ./level13, we get:

```bash
UID 2013 started us but we expect 4242
```

This means the program checks if the user's UID is 4242 (0x1092 in hex) before giving the token.

## Step 2: Reverse Engineering (Decompilation)

Using [Dogbolt](https://dogbolt.org), we decompile main():

```bash
void main(void) {
  __uid_t uid = getuid();

  if (uid != 0x1092) {  // 0x1092 = 4242 in decimal
    printf("UID %d started us but we expect %d\n", uid, 0x1092);
    exit(1);
  }

  char *token = ft_des("boe]!ai0FB@.:|L6l@A?>qJ}I");
  printf("your token is %s\n", token);
}
```

- The program checks if the current UID is 4242.
- If not, it prints an error and exits.
- If yes, it decrypts a hidden token using ft_des().

## Step 3: Bypass the UID Check

Since we don’t have UID 4242, we need to skip the check and jump directly to the part where ft_des() is called.

### Using GDB:

1. Disassemble main:

```bash
gdb ./level13
(gdb) disassemble main
```

Output:

```bash
Dump of assembler code for function main:
   0x0804858c <+0>:     push   %ebp
   0x0804858d <+1>:     mov    %esp,%ebp
   0x0804858f <+3>:     and    $0xfffffff0,%esp
   0x08048592 <+6>:     sub    $0x10,%esp
   0x08048595 <+9>:     call   0x8048380 <getuid@plt>
   0x0804859a <+14>:    cmp    $0x1092,%eax
   0x0804859f <+19>:    je     0x80485cb <main+63>  ; Jump if UID == 4242
   0x080485a1 <+21>:    call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:    mov    $0x80486c8,%edx
   0x080485ab <+31>:    movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:    mov    %eax,0x4(%esp)
   0x080485b7 <+43>:    mov    %edx,(%esp)
   0x080485ba <+46>:    call   0x8048360 <printf@plt>
   0x080485bf <+51>:    movl   $0x1,(%esp)
   0x080485c6 <+58>:    call   0x80483a0 <exit@plt>
   0x080485cb <+63>:    movl   $0x80486ef,(%esp)  ; Calls ft_des()
   0x080485d2 <+70>:    call   0x8048474 <ft_des>
   0x080485d7 <+75>:    mov    $0x8048709,%edx
   0x080485dc <+80>:    mov    %eax,0x4(%esp)
   0x080485e0 <+84>:    mov    %edx,(%esp)
   0x080485e3 <+87>:    call   0x8048360 <printf@plt>
   0x080485e8 <+92>:    leave
   0x080485e9 <+93>:    ret
```

2. Set a Breakpoint Before the Check:

```bash
(gdb) break *0x0804859f
Breakpoint 1 at 0x804859f
```

3. Run the Program:

```bash
(gdb) run
```

4. Jump Over the Check:

```bash
(gdb) jump *0x080485cb
```

This forces execution to skip the UID check and go straight to ft_des().

5. Get the Token:

```text
Continuing at 0x80485cb.
your token is 2A31L79asukciNyi8uppkEuSx
```

## Next Steps

With the flag 2A31L79asukciNyi8uppkEuSx, we can now proceed to Level14 of the SnowCrash challenge.
