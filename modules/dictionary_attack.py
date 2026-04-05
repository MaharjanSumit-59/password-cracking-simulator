import time
from modules.hasher import hash_sha256

def dictionary_attack(target_hash: str, wordlist_path: str, hash_func=hash_sha256) -> dict:
    """
    Tries passwords from a wordlist file.
    
    Real attackers use wordlists with millions of common passwords.
    This is why 'password123' is never safe — it's always in the list.
    """
    
    start_time = time.time()
    attempts = 0
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                candidate = line.strip()  # Remove newline characters
                
                if not candidate:  # Skip empty lines
                    continue
                
                attempts += 1
                
                if hash_func(candidate) == target_hash:
                    elapsed = time.time() - start_time
                    return {
                        "success": True,
                        "password": candidate,
                        "attempts": attempts,
                        "time_seconds": round(elapsed, 4),
                        "method": "Dictionary Attack"
                    }
    
    except FileNotFoundError:
        return {"error": f"Wordlist not found: {wordlist_path}"}
    
    elapsed = time.time() - start_time
    return {
        "success": False,
        "password": None,
        "attempts": attempts,
        "time_seconds": round(elapsed, 4),
        "method": "Dictionary Attack"
    }


