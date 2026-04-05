import re
import string
from zxcvbn import zxcvbn  # Dropbox's password strength library

def check_strength(password: str) -> dict:
    """
    Analyzes password strength using multiple methods.
    zxcvbn gives a score 0-4:
    0 = Very weak, 4 = Very strong
    """
    
    # Use zxcvbn for smart analysis (it detects patterns, common words, etc.)
    result = zxcvbn(password)
    
    # Also do our own rule-based analysis
    rules = {
        "length_8": len(password) >= 8,
        "length_12": len(password) >= 12,
        "has_lowercase": bool(re.search(r'[a-z]', password)),
        "has_uppercase": bool(re.search(r'[A-Z]', password)),
        "has_digit": bool(re.search(r'\d', password)),
        "has_special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "no_common_patterns": not _has_common_pattern(password)
    }
    
    score_map = {0: "Very Weak 🔴", 1: "Weak 🟠", 2: "Fair 🟡", 3: "Strong 🟢", 4: "Very Strong 💪"}
    
    return {
        "password": password,  # In real systems, NEVER log/return the password!
        "score": result['score'],
        "score_label": score_map[result['score']],
        "crack_time_display": result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        "feedback": result['feedback'],
        "rules_passed": rules,
        "rules_score": f"{sum(rules.values())}/{len(rules)}"
    }


def _has_common_pattern(password: str) -> bool:
    """Detects obviously weak patterns."""
    patterns = [
        r'(.)\1{2,}',       # Repeated chars: aaa, 111
        r'(012|123|234|345|456|567|678|789)',  # Sequential numbers
        r'(abc|bcd|cde|def)',  # Sequential letters
    ]
    return any(re.search(p, password.lower()) for p in patterns)