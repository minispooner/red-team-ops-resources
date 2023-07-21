# Exfiltration

__TTP of Threat Actors Exploiting Citrix CVE-2023-3519__
```
tar -czvf - /var/tmp/data.txt | openssl des3 -salt -k <> -out /var/tmp/test.tar.gz
cp /var/tmp/test.tar.gz /var/www/html/images/medialogininit.png
```
