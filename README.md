# bash-tools
quick bash tools for pentest work

### Loop file lines
```
#!/bin/bash
  
while read host; do
    filename="$(echo $host | sed "s/https:\/\///g" | sed "s/http:\/\///g")"
    curl -s -v -k -m 3 $host > $filename
    echo "scanned $host"
done < $1
```
