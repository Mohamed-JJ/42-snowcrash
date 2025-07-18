# SnowCrash Level02 Walkthrough

## Overview
Level02 involves analyzing a packet capture file to extract authentication credentials hidden in network traffic.

## Initial Investigation

First, let's examine what files are available in the home directory:

```bash
level02@SnowCrash:~$ ls
level02.pcap
```

We discover a `.pcap` file, which is a Packet Capture file that stores network traffic information. These files capture raw network packet data, including headers and payloads, enabling detailed analysis of network activity.

## File Transfer and Analysis Setup

To analyze the packet capture file, we need to transfer it to our analysis machine (Kali Linux) where we have Wireshark installed.

### Step 1: Transfer from SnowCrash to local machine

```bash
scp -P 4242 level02@192.168.56.101:/home/user/level02/level02.pcap .
```

### Step 2: Set appropriate permissions

```bash
chmod 777 level02.pcap
```

### Step 3: Transfer to Kali Linux

```bash
scp ./level02.pcap kali@10.13.100.25:/home/kali/
```

## Wireshark Analysis

### Opening the Capture File

Launch Wireshark and load the `level02.pcap` file. We'll analyze the network traffic to look for potential authentication credentials.

### Searching for Credentials

1. Use Wireshark's search functionality to look for plaintext credentials
2. Search for common authentication-related keywords like "password", "login", "user", etc.

### Finding the Password

After searching through the packets, we locate interesting data containing password information:

![Password packet discovery](image.png)

### Following the TCP Stream

1. Right-click on the packet containing the password data
2. Select "Follow" → "TCP Stream"

![Follow TCP Stream option](image-1.png)

This reveals the complete conversation in a readable format:

![TCP Stream with password](image-2.png)

## Password Extraction and Analysis

From the TCP stream, we can extract what appears to be the password: `ft_wandr...NDRel.L0L.`

### Initial Authentication Attempt

```bash
level02@SnowCrash:~$ su flag02
Password: ft_wandr...NDRel.L0L.
su: Authentication failure
```

The authentication fails, indicating the password isn't correct as extracted.

### Hex Analysis

Upon closer inspection of the hex values in Wireshark, we discover that some characters are non-printable control characters:

- `7f` → DEL (Delete character)
- `0d` → CR (Carriage Return)

These control characters represent backspace operations and line endings that affected the password input.

### Password Reconstruction

After accounting for the control characters and their effects on the input, the actual password becomes:

**`ft_waNDReL0L`**

The reconstruction process:
- `ft_w` - initial characters
- `a` - character typed
- `DEL` - backspace (removes the 'a')
- `a` - character retyped
- `n` - next character
- `d` - character typed
- `DEL` - backspace (removes the 'd')
- `D` - character retyped (uppercase)
- `r` - character typed
- `DEL` - backspace (removes the 'r')
- `R` - character retyped (uppercase)
- `e` - next character
- `l` - character typed
- `DEL` - backspace (removes the 'l')
- `L` - character retyped (uppercase)
- `0L` - final characters

## Final Authentication

```bash
level02@SnowCrash:~$ su flag02
Password: ft_waNDReL0L
Don't forget to launch getflag !
```

### Retrieving the Flag

```bash
flag02@SnowCrash:~$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
```

## Key Learnings

1. **Network Traffic Analysis**: Packet capture files can contain sensitive information like passwords transmitted in plaintext
2. **Control Characters**: Non-printable characters in network traffic can affect password reconstruction
3. **Hex Interpretation**: Understanding hexadecimal values is crucial for proper data extraction
4. **Tools**: Wireshark's TCP stream following feature is invaluable for reconstructing network conversations

## Flag
```
kooda2puivaav1idi4f57q8iq
```

This flag can be used to access the next level of the SnowCrash challenge.