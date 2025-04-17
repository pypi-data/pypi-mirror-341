import platform
import socket

def get_system_info():
    """
    Gather basic system information.
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor()
    }

def get_network_info():
    """
    Gather network hostname and local IP.
    """
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = 'Unknown'
    return {"hostname": hostname, "ip": ip}