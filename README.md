This is a Python script I created to rotate the public-facing IP address. It's quite simple, just monitoring for lost pings or failed website connections.

Checks for everything with seleniumm & wait.until

Unfortunately, the router takes some time to reboot, but it consistently assigns a different public IP address and avoids placing users behind a CGNAT IP.

```pip import subprocess```
```pip import selenium```
```pip import requests```
```pip import asyncio```
```pip import time```

<3
