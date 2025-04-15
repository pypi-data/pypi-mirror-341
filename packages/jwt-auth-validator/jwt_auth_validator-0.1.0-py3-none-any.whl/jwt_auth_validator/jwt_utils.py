import jwt
from jwt import InvalidTokenError
import requests
import json

# کش برای ذخیره کلید عمومی
public_key_cache = {}

def get_public_key(jwks_url, kid):
    # اول چک می‌کنیم آیا public key توی کش موجوده یا نه
    if kid in public_key_cache:
        return public_key_cache[kid]

    # در غیر اینصورت باید JWKS رو دانلود کنیم
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch JWKS")
    
    jwks = response.json()
    key = None
    for k in jwks['keys']:
        if k['kid'] == kid:
            key = k
            break
    
    if key is None:
        raise Exception(f"Key with kid {kid} not found in JWKS")

    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    public_key_cache[kid] = public_key  # ذخیره‌سازی در کش
    return public_key

def decode_token(token, jwks_url):
    try:
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header is None:
            raise Exception("Invalid JWT Token")

        kid = unverified_header.get("kid")
        if kid is None:
            raise Exception("Missing kid in JWT header")
        
        public_key = get_public_key(jwks_url, kid)
        payload = jwt.decode(token, public_key, algorithms=["RS256"], options={"verify_aud": False})
        return payload

    except InvalidTokenError as e:
        raise Exception(f"Invalid token: {str(e)}")