from flask import Flask, render_template, request, jsonify
from modules.hasher import hash_sha256, hash_md5, hash_bcrypt
from modules.brute_force import brute_force_attack, estimate_brute_force_time
from modules.dictionary_attack import dictionary_attack
from modules.strength_checker import check_strength
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/hash', methods=['POST'])
def hash_password():
    """Hash a password using chosen algorithm."""
    data = request.json
    password = data.get('password', '')
    algorithm = data.get('algorithm', 'sha256')
    
    if algorithm == 'sha256':
        hashed = hash_sha256(password)
    elif algorithm == 'md5':
        hashed = hash_md5(password)
    elif algorithm == 'bcrypt':
        hashed = hash_bcrypt(password).decode()
    
    return jsonify({"hash": hashed, "algorithm": algorithm})


@app.route('/api/brute-force', methods=['POST'])
def run_brute_force():
    data = request.json
    target_hash = data.get('hash', '')
    max_length = min(int(data.get('max_length', 4)), 4)
    algorithm = data.get('algorithm', 'sha256')

    # Select correct hash function
    if algorithm == 'md5':
        selected_hash_func = hash_md5
    elif algorithm == 'bcrypt':
        selected_hash_func = hash_bcrypt
    else:
        selected_hash_func = hash_sha256

    result = brute_force_attack(
        target_hash=target_hash,
        charset=string.ascii_lowercase + string.digits,
        max_length=max_length,
        hash_func=selected_hash_func,
        algorithm=algorithm          # ← pass algorithm too!
    )
    return jsonify(result)



@app.route('/api/dictionary', methods=['POST'])
def run_dictionary():
    """Run dictionary attack simulation."""
    data = request.json
    target_hash = data.get('hash', '')
    
    result = dictionary_attack(
        target_hash=target_hash,
        wordlist_path='data/wordlist.txt'
    )
    return jsonify(result)


@app.route('/api/strength', methods=['POST'])
def password_strength():
    """Check password strength."""
    data = request.json
    password = data.get('password', '')
    
    result = check_strength(password)
    return jsonify(result)


@app.route('/api/estimate', methods=['POST'])
def estimate_crack_time():
    """Estimate cracking time without actually cracking."""
    data = request.json
    password = data.get('password', '')
    
    result = estimate_brute_force_time(password)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)