# Windows Snippets

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
