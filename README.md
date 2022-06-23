# bash-tools
quick bash tools

### Loop file lines
```
#!/bin/bash
  
while read host; do
    filename="$(echo $host | sed "s/https:\/\///g" | sed "s/http:\/\///g")"
    echo "scanned $host"
    # output_command > $filename
done < $1
```
