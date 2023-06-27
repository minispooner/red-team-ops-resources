a# Pivoting

## SSH
`ssh -i privkey -L LOCALPORT:TARGETIP:TARGETPORT USER@JUMPBOX` then run tools against localhost:LOCALPORT and they will be run against the TARGETIP:TARGETPORT on the other network that the JUMPBOX can reach.

## Meterpreter
### Routes and SOCKS proxychains
- https://infinitelogins.com/2021/02/20/using-metasploit-routing-and-proxychains-for-pivoting/
