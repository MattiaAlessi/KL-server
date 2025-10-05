import subprocess
import re

def get_ipv4():
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        output = result.stdout
        match = re.search(r"IPv4.*?:\s*([\d\.]+)", output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

ip_address = get_ipv4()

if ip_address:
    with open("ip_address.txt", "w") as file:
        file.write(ip_address)
