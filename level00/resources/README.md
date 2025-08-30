# SnowCrash Level00 Walkthrough

## Overview
Level00 is an introductory challenge that focuses on basic file system exploration and cryptography. The goal is to find hidden files and decode encrypted content to obtain access credentials.

## Objective
- Explore the file system to find files owned by specific users
- Decode encrypted content to reveal a password
- Use the password to switch users and retrieve the flag

## Solution Steps

### 1. Initial Reconnaissance
Start by exploring files owned by the current user `level00`:

```bash
find / -user level00 2>/dev/null
```

**Result**: Only proc-related files are found, which are not useful for this challenge.

### 2. Searching for Flag-Related Files
Search for files owned by the target user `flag00`:

```bash
find / -user flag00 2>/dev/null
```

**Result**: Two interesting files are discovered:
```
/usr/sbin/john
/rofs/usr/sbin/john
```

### 3. Examining the Files
Display the content of both files:

```bash
level00@SnowCrash:~$ cat /usr/sbin/john /rofs/usr/sbin/john
cdiiddwpgswtgt
cdiiddwpgswtgt
level00@SnowCrash:~$ 
```

**Observation**: Both files contain the same encrypted string: `cdiiddwpgswtgt`

### 4. Cryptographic Analysis
The string appears to be encrypted using a substitution cipher. Using online cipher analysis tools (such as [CacheSleuth Multi Decoder](https://www.cachesleuth.com/multidecoder/)), we can identify this as a **Caesar cipher with ROT15**.

![alt text](<Screenshot from 2025-07-12 18-08-20.png>)

**Decryption Process**:
- Original: `cdiiddwpgswtgt`
- Cipher type: Caesar cipher (ROT15)
- **Decrypted**: `nottoohardhere`

### 5. User Authentication
Use the decoded password to switch to the `flag00` user:

```bash
level00@SnowCrash:~$ su flag00
Password: nottoohardhere
Don't forget to launch getflag !
flag00@SnowCrash:~$ 
```

### 6. Flag Retrieval
Execute the `getflag` command to obtain the token:

```bash
flag00@SnowCrash:~$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
flag00@SnowCrash:~$ 
```

## Key Concepts Learned

### File System Exploration
- Using `find` command to locate files by ownership
- Understanding file permissions and access rights
- Redirecting error output with `2>/dev/null`

### Cryptography
- **Caesar Cipher**: A substitution cipher where each letter is shifted by a fixed number of positions
- **ROT15**: A specific Caesar cipher with a shift of 15 positions
- Importance of cipher identification in penetration testing

### Linux Commands Used
- `find / -user <username> 2>/dev/null` - Find files owned by a specific user
- `cat <file>` - Display file contents
- `su <username>` - Switch to another user
- `getflag` - SnowCrash-specific command to retrieve flags

## Tools and Resources
- **CacheSleuth Multi Decoder**: Online tool for cipher analysis and decryption
- **Alternative tools**: CyberChef, dcode.fr, or manual ROT analysis

## Security Insights
This level demonstrates:
- How sensitive information can be hidden in unexpected locations
- The importance of proper file permissions
- Basic cryptographic techniques used in CTF challenges
- The value of systematic file system enumeration

## Final Token
```
x24ti5gi3x0ol2eh4esiuxias
```

---

**Next Step**: Use this token to access Level01 of the SnowCrash challenge series.