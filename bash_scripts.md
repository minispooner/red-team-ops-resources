# quick bash scripts
quick bash tools for pentest work

## Loop file lines (one-liner)
```
while read host; do echo "Scanning $host..." && COOL_TOOL $host; done<hostsfile.txt
```

## Loop file lines
```
#!/bin/bash
  
while read host; do
    filename="$(echo $host | sed "s/https:\/\///g" | sed "s/http:\/\///g")"
    curl -s -v -k -m 3 $host > $filename
    echo "scanned $host"
done < $1
```

## Keep a processs running while you're not SSHd in
1. SSH into your server
2. run `tmux attach` to enter a tmux session
3. start your scanner, script, automation, etc
4. hit `ctr+b` then `d` to leave the session without killing it
5. exit your SSH session. go pound cheetos
6. reconnect your SSH session
7. run `tmux attach` to enter your previous tmux session

You can also have and name multiple tmux sessions. Google it.
