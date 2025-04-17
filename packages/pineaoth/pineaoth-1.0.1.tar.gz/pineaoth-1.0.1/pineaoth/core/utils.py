import base64

def is_valid_base32(secret):
    try:
        base64.b32decode(secret, casefold=True)
        return True
    except Exception:
        return False
