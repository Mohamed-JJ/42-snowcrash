# SnowCrash Level09 Walkthrough

## Overview

Level09 presents a **custom encryption challenge** involving a simple substitution cipher. The task requires reverse-engineering an encryption algorithm and implementing its decryption counterpart to recover a hidden token.

## Initial Reconnaissance

In the home directory, we find two files:

```bash
level09@SnowCrash:~$ ls -la
total 24
dr-x------ 1 level09 level09  140 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level09 level09  220 Apr  3  2012 .bash_logout
-r-x------ 1 level09 level09 3518 Aug 30  2015 .bashrc
-rwsr-sr-x 1 flag09  level09 7640 Mar  5  2016 level09
-r-x------ 1 level09 level09  675 Apr  3  2012 .profile
----r--r-- 1 flag09  level09   26 Mar  5  2016 token
```

Key observations:
- `level09`: An executable with SUID bit set
- `token`: A file containing encrypted data

## Analyzing the Encrypted Token

Let's examine the content of the token file:

```bash
level09@SnowCrash:~$ cat token
f4kmm6p|=�p�n��DB�Du{��
```

The output contains non-printable characters and appears to be encrypted or encoded data.

## Reverse Engineering the Encryption

### Basic Program Behavior

Testing the executable reveals its functionality:

```bash
level09@SnowCrash:~$ ./level09
You need to provied only one arg.

level09@SnowCrash:~$ ./level09 hello
hfnos
```

The program requires exactly one argument and appears to encrypt the input string.

### Pattern Analysis

Let's test with predictable input to understand the encryption algorithm:

```bash
level09@SnowCrash:~$ ./level09 "abcdefgh"
acegikmo

level09@SnowCrash:~$ ./level09 123456789
13579;=?A
```

### Algorithm Discovery

Analyzing the patterns:

**Test Case 1**: `"abcdefgh"` → `"acegikmo"`
- `a` (pos 0, ASCII 97) → `a` (ASCII 97) | 97 + 0 = 97 ✓
- `b` (pos 1, ASCII 98) → `c` (ASCII 99) | 98 + 1 = 99 ✓
- `c` (pos 2, ASCII 99) → `e` (ASCII 101) | 99 + 2 = 101 ✓
- `d` (pos 3, ASCII 100) → `g` (ASCII 103) | 100 + 3 = 103 ✓

**Algorithm Identified**: Each character is shifted by its position index in the string.

```
encrypted_char = original_char + position_index
```

## Decryption Implementation

### Python Decryption Script

Now we can create a script to reverse the encryption:

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) < 2:
    print("Usage: python decrypt.py <encrypted_string>")
    sys.exit(1)

encrypted_text = sys.argv[1]
decrypted = ''

for i in range(len(encrypted_text)):
    # Get ASCII value of current character
    encrypted_ascii = ord(encrypted_text[i])
    
    # Subtract the position index to decrypt
    decrypted_ascii = encrypted_ascii - i
    
    # Convert back to character
    decrypted += chr(decrypted_ascii)

print(decrypted)
```

### Creating and Using the Decryption Script

```bash
level09@SnowCrash:~$ cat > /tmp/decrypt.py << 'EOF'
#!/usr/bin/env python3
import sys

if len(sys.argv) < 2:
    print("Usage: python decrypt.py <encrypted_string>")
    sys.exit(1)

encrypted_text = sys.argv[1]
decrypted = ''

for i in range(len(encrypted_text)):
    encrypted_ascii = ord(encrypted_text[i])
    decrypted_ascii = encrypted_ascii - i
    decrypted += chr(decrypted_ascii)

print(decrypted)
EOF

level09@SnowCrash:~$ chmod +x /tmp/decrypt.py
```

## Token Decryption

### Extracting and Decrypting the Token

```bash
level09@SnowCrash:~$ cat token | xargs python /tmp/decrypt.py
f3iji1ju5yuevaus41q1afiuq
```

### Verification

Let's verify our decryption by re-encrypting the result:

```bash
level09@SnowCrash:~$ ./level09 "f3iji1ju5yuevaus41q1afiuq"
f4kmm6p|=�p�n��DB�Du{��

level09@SnowCrash:~$ cat token
f4kmm6p|=�p�n��DB�Du{��
```

✅ **Perfect match!** The decryption is correct.

## Flag Retrieval

### Switching to flag09 User

```bash
level09@SnowCrash:~$ su flag09
Password: f3iji1ju5yuevaus41q1afiuq
Don't forget to launch getflag !
```

### Getting the Final Flag

```bash
flag09@SnowCrash:~$ getflag
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

## Success!

We successfully decrypted the token and obtained the flag: `s5cAJpM8ev6XHw998pRWG728z`

## Technical Analysis

### Encryption Algorithm Breakdown

```
Position: 0  1  2  3  4  5  6  7
Input:    f  3  i  j  i  1  j  u
ASCII:   102 51 105 106 105 49 106 117
Add Pos: +0 +1 +2  +3  +4 +5 +6  +7
Result:  102 52 107 109 109 54 112 124
Output:   f  4  k  m  m  6  p  |
```

### Key Insights

1. **Simple Substitution**: Each character is shifted by its zero-based position
2. **Reversible**: The encryption is easily reversible by subtracting the position
3. **Position-Dependent**: The same character encrypts differently based on its position
4. **ASCII-Based**: Works directly on ASCII values

## Cryptographic Analysis

### Strengths
- Position-dependent encryption provides some variation
- Simple to implement

### Weaknesses
- **Extremely weak**: Pattern is easily discoverable with minimal plaintext
- **No key**: The algorithm is completely deterministic
- **Linear progression**: The shift amount follows a predictable pattern
- **Frequency analysis**: Still vulnerable to cryptanalytic attacks

## Key Learning Points

1. **Reverse Engineering**: Always test with predictable input to understand algorithms
2. **Pattern Recognition**: Simple encryption schemes often have discoverable patterns
3. **Verification**: Always verify decryption by re-encrypting the result
4. **Weak Cryptography**: Position-based shifts are cryptographically weak
5. **SUID Exploitation**: The encrypted token likely contains credentials for privilege escalation

## Security Implications

This challenge demonstrates why:
- Custom encryption should never be used in production
- Established cryptographic libraries should be preferred
- Security through obscurity is ineffective
- Even simple obfuscation can be quickly reversed with proper analysis

## Next Steps

With the flag `s5cAJpM8ev6XHw998pRWG728z`, we can now proceed to Level10 of the SnowCrash challenge.