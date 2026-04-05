import hashlib
import bcrypt
import os

def hash_sha256(password: str) -> str:
    """
    Hash a password using SHA-256.
    Simple, fast — but NOT recommended for real passwords.
    Good for demonstration purposes.
    """
    # encode() converts string to bytes (SHA256 needs bytes)
    return hashlib.sha256(password.encode()).hexdigest()


def hash_md5(password: str) -> str:
    """
    Hash using MD5 — intentionally weak, shown for comparison.
    NEVER use MD5 for real passwords.
    """
    return hashlib.md5(password.encode()).hexdigest()


def hash_bcrypt(password: str) -> bytes:
    """
    Hash using bcrypt — the CORRECT way to hash passwords.
    bcrypt is slow by design, making brute force very hard.
    
    'rounds' = how many times it processes the hash.
    More rounds = slower to compute = harder to crack.
    """
    salt = bcrypt.gensalt(rounds=12)  # 12 is the recommended default
    return bcrypt.hashpw(password.encode(), salt)


def verify_bcrypt(password: str, hashed: bytes) -> bool:
    """
    Check if a plain password matches a bcrypt hash.
    bcrypt handles the salt comparison internally.
    """
    return bcrypt.checkpw(password.encode(), hashed)


def hash_sha256_with_salt(password: str, salt: str = None) -> tuple:
    """
    Demonstrates manual salting with SHA-256.
    Salt = random string added to password before hashing.
    Prevents 'rainbow table' attacks.
    """
    if salt is None:
        # Generate a random 16-byte salt, convert to hex string
        salt = os.urandom(16).hex()
    
    salted_password = salt + password  # Combine salt + password
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed, salt  # Return both — you need the salt to verify later!