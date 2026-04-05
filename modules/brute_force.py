import itertools
import string
import time

import bcrypt
from modules.hasher import hash_sha256
def brute_force_attack(
    target_hash: str,
    charset: str = string.ascii_lowercase + string.digits,  # ← added numbers
    max_length: int = 4,                                    # ← changed 4 to 5
    hash_func = hash_sha256,
    algorithm: str = 'sha256'    # ← NEW parameter
) -> dict:
    """
    Simulates a brute force attack by trying every combination.
    
    Parameters:
    - target_hash: the hash we're trying to crack
    - charset: which characters to try (default: a-z)
    - max_length: maximum password length to try
    - hash_func: which hashing algorithm was used
    
    Returns a dictionary with results.
    """
    
    start_time = time.time()  # Record when we started
    attempts = 0
    
# bcrypt is VERY slow by design
    # warn user if they try bcrypt brute force
    '''    
            Brute forcing a 4-char password:
            SHA256 → fraction of a second  ✅
            bcrypt → 4.6 hours             ❌ browser would timeout!
    '''
    
    if algorithm == 'bcrypt':
        return {
            "success": False,
            "password": None,
            "attempts": 0,
            "time_seconds": 0,
            "method": "Brute Force",
            "warning": "⚠️ bcrypt is intentionally too slow for brute force simulation. This demonstrates WHY bcrypt is secure!"
        }

    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):

            attempts += 1
            candidate = ''.join(combo)

            # Handle different algorithms differently:
            if algorithm == 'bcrypt':
                try:
                    is_match = bcrypt.checkpw(
                        candidate.encode(),
                        target_hash.encode()
                    )
                except Exception:
                    is_match = False
            else:
                # Normal comparison for MD5/SHA256
                is_match = hash_func(candidate) == target_hash

            if is_match:
                elapsed = time.time() - start_time
                return {
                    "success": True,
                    "password": candidate,
                    "attempts": attempts,
                    "time_seconds": round(elapsed, 4),
                    "method": "Brute Force"
                }

    elapsed = time.time() - start_time
    return {
        "success": False,
        "password": None,
        "attempts": attempts,
        "time_seconds": round(elapsed, 4),
        "method": "Brute Force"
    }


def estimate_brute_force_time(password: str, attempts_per_second: int = 1_000_000) -> dict:
    """
    Estimates how long brute force would take WITHOUT actually doing it.
    This is safe — it's just math.
    
    Real GPU hashcracking speeds (for education):
    - MD5:    ~10 billion/sec
    - SHA256: ~3 billion/sec  
    - bcrypt: ~10,000/sec  ← This is why bcrypt wins
    """
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32
    
    length = len(password)
    
    # Total combinations = charset_size ^ length
    total_combinations = charset_size ** length
    
    # Worst case: try every combination
    seconds = total_combinations / attempts_per_second
    
    return {
        "password_length": length,
        "charset_size": charset_size,
        "total_combinations": total_combinations,
        "estimated_seconds": seconds,
        "human_readable": _seconds_to_human(seconds)
    }


def _seconds_to_human(seconds: float) -> str:
    """Converts seconds into human-readable time."""
    if seconds < 1:
        return "Less than 1 second"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2e} years"  # Scientific notation for huge numbers