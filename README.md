# bash-tools
quick bash tools

### Loop file lines
```
#!/bin/bash
  
while read host; do
        echo "scanned $host"
done < $1
```
