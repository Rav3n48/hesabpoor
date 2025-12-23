import os
import hashlib
import hmac


ALGORITHM = "pbkdf2_sha256" # Hashing algorithm
REPEATS = 150000 # How many times password gets hashed
SALT_LENGTH = 16
KEY_LENGTH = 32


# Hashing function, return format: algorithm$repeats$salt_hex$hash_hex
def hash_password(password):
    # Generate a random salt
    salt = os.urandom(SALT_LENGTH)

    # Extract the key using PBKDF2-HMAC-SHA256
    extracted_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        REPEATS,
        dklen=KEY_LENGTH,
    )

    salt_hex = salt.hex()
    hash_hex = extracted_key.hex()

    return f"{ALGORITHM}${REPEATS}${salt_hex}${hash_hex}"

# Compares given password and stored hash and returns boolean
def verify_password(password, stored_hash):

    algorithm, repeats_str, salt_hex, hash_hex = stored_hash.split("$", 3)

    if algorithm != ALGORITHM:
        pass # For later changes

    repeats = int(repeats_str)

    salt = bytes.fromhex(salt_hex)
    original_hash = bytes.fromhex(hash_hex)

    # Extract key with same parameters
    extracted_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        repeats,
        dklen=len(original_hash),
    )

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(extracted_key, original_hash)
