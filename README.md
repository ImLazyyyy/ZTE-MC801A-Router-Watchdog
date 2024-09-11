This is a Python script I created to rotate the public-facing IP address. It's quite simple, just monitoring for lost pings or failed website connections using selenium to login to the web UI, going to settings, APN, then changing the APN once packet's have been detected as lost.

Checks for everything with seleniumm & wait.until

Unfortunately, the router takes some time to reboot, but it consistently assigns a different public IP address and avoids placing users behind a CGNAT IP.

If you are looking just for an IP address changer, I have that too. 

https://github.com/ImLazyyyy/ZTE-MC801A-Quick-IP-address-Changer

```pip import subprocess```
```pip import selenium```
```pip import requests```
```pip import asyncio```
```pip import time```

<3
