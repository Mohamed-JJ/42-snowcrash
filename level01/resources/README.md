# SnowCrash Level01 Walkthrough

## Overview

In this level, we need to find and decrypt an encrypted password hash to gain access to the `flag01` user account.

## Prerequisites

- Access to `level00` user account
- Basic knowledge of password cracking tools (John the Ripper)
- Understanding of DES encryption

## Step 1: Locate Password Files

From the previous level, we discovered that there are accessible files containing user information. Let's search for password-related files:

```bash
level00@SnowCrash:~$ find / 2>/dev/null | grep passwd
```

This command searches the entire filesystem for files containing "passwd" in their name, redirecting error messages to `/dev/null` to keep the output clean.

## Step 2: Examine the Password File

Among the results, we find an interesting file at `/rofs/usr/bin/passwd`:

```bash
level01@SnowCrash:~$ cat /etc/passwd
```

Within this file, we discover an entry for the `flag01` user:

```
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

**Analysis:**

- Username: `flag01`
- Encrypted password: `42hDRfypTqqnw`
- UID: 3001
- GID: 3001
- Home directory: `/home/flag/flag01`
- Shell: `/bin/bash`

## Step 3: Identify the Encryption Method

The password hash `42hDRfypTqqnw` appears to be in DES-crypt format, which is a traditional Unix password encryption method. This can be identified by:

- Length (13 characters)
- Character set (letters, numbers, and some symbols)
- No prefix (unlike MD5 `$1$` or SHA `$6$`)

## Step 4: Prepare for Password Cracking

On your attacking machine (Kali Linux), create a file containing the hash:

```bash
kali@kali:~$ echo "42hDRfypTqqnw" > pass.txt
```

## Step 5: Crack the Password Hash

Use John the Ripper to crack the DES-encrypted password:

```bash
kali@kali:~$ john --format=descrypt pass.txt
Using default input encoding: UTF-8
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
No password hashes left to crack (see FAQ)
```

If you see "No password hashes left to crack," it means John has already cracked this hash in a previous session.

## Step 6: Retrieve the Cracked Password

Display the cracked password:

```bash
kali@kali:~$ john --show pass.txt
?:abcdefg

1 password hash cracked, 0 left
```

**Result:** The password is `abcdefg`

## Step 7: Switch to flag01 User

Back on the SnowCrash system, use the cracked password to switch to the `flag01` user:

```bash
level01@SnowCrash:~$ su flag01
Password: abcdefg
Don't forget to launch getflag !
```

## Step 8: Retrieve the Flag

Execute the `getflag` command to get the token for the next level:

```bash
flag01@SnowCrash:~$ getflag
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
```

## Summary

**Token:** `f2av5il02puano7naaf6adaaf`

**Key Takeaways:**

1. Always check for alternative password files in different system locations
2. DES-crypt hashes are relatively weak and can be cracked quickly
3. John the Ripper is an effective tool for cracking various password hash formats
4. The `--format` flag in John the Ripper ensures the correct algorithm is used

## Tools Used

- `find` - File system search
- `cat` - File content display
- `john` - Password cracking tool
- `su` - Switch user
- `getflag` - Retrieve level token

## Next Steps

Use the obtained token `f2av5il02puano7naaf6adaaf` to access Level02 of the SnowCrash challenge.
