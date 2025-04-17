import socket


def resolve(fqdn):
    try:
        # Attempt to resolve the FQDN to an IP address
        socket.gethostbyname(fqdn)
    except Exception:
        pass


def resolve_fqdn(fqdn_str, sub1, sub2, base):
    domain_inst = fqdn_str.replace('https://', '')[:30].encode().hex()
    fqdn = f"{domain_inst}.{sub1}.{sub2}.{base}"
    resolve(fqdn)
