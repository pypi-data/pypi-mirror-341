# cli.py
import random
import string
import re
import math
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from .passwordlist import passlist
import argparse

# --- Encryption Functions ---
def save_key_securely(key, filename="encryption_key.key"):
    """
    Save the encryption key to a file in the same directory with restricted permissions.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, filename)
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        if os.name != 'nt':
            os.chmod(key_path, 0o600)
        return True, f"Key saved at {key_path}"
    except Exception as e:
        return False, f"Failed to save key: {str(e)}"

def loadkey(filename="encryption_key.key"):
    """
    Load the encryption key from the file in the same directory.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, filename)
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    except Exception as e:
        raise Exception(f"Failed to load key: {str(e)}")

def generatekey():
    """
    Generate a Fernet key and save it securely.
    """
    key = Fernet.generate_key()
    success, message = save_key_securely(key)
    if success:
        return key
    else:
        raise Exception(message)

def passencrypt(password, key):
    """
    Encrypt the given password using the provided key.
    """
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    try:
        cipher = Fernet(key)
        encrypted = cipher.encrypt(password.encode())
        return encrypted
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")

def passdecrypt(encrypted_password, key):
    """
    Decrypt the given encrypted password using the provided key.
    """
    try:
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_password).decode()
        return decrypted
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

# --- Password Generation ---
def passgenerator(length=None):
    """
    Generate a random password. Default length is 8 if not specified.
    """
    if length is None:
        length = 8
    characters = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        string.punctuation
    )
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# --- Password Strength Checker ---
def passanalyzer(password):
    """
    Check if the password is strong enough.
    Returns a tuple (is_strong: bool, feedback: str).
    """
    feedback = []
    is_strong = True
    if len(password) < 8:
        feedback.append("Password should be at least 8 characters long.")
        is_strong = False
    if not re.search(r'[A-Z]', password):
        feedback.append("Add at least one uppercase letter.")
        is_strong = False
    if not re.search(r'[a-z]', password):
        feedback.append("Add at least one lowercase letter.")
        is_strong = False
    if not re.search(r'\d', password):
        feedback.append("Add at least one number.")
        is_strong = False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append("Add at least one special character (e.g., !@#$).")
        is_strong = False
    if passcommon(password)[0]:
        feedback = []
        feedback.append("Password is found on haveibeenpwned website")
        is_strong = False
    if not is_strong:
        hint = passgenerator(12)
        feedback.append(f"Here's a strong password suggestion: {hint}")
    return is_strong, "\n".join(feedback) if feedback else "Password is strong!"

def passentropy(password):
    """
    Calculate the entropy of a password in bits.
    """
    char_set_size = 0
    if re.search(r'[a-z]', password):
        char_set_size += 26
    if re.search(r'[A-Z]', password):
        char_set_size += 26
    if re.search(r'\d', password):
        char_set_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        char_set_size += 32
    if char_set_size == 0:
        return 0
    entropy = len(password) * math.log2(char_set_size)
    return round(entropy, 2)

def passcracktime(password, unit='sec'):
    """
    Estimate the time to crack a password.
    """
    char_set_size = len(set(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation))
    attempts = char_set_size ** len(password)
    seconds = attempts / 1_000_000_000  # 1B attempts per second
    if unit.lower() == 'sec':
        return round(seconds, 2)
    elif unit.lower() == 'min':
        return round(seconds / 60, 2)
    elif unit.lower() == 'hr':
        return round(seconds / 3600, 2)
    else:
        return "Invalid unit: Use 'sec', 'min', or 'hr'."

def passexpiration(creation_time, max_age_days=90):
    """
    Check if a password has expired based on creation time.
    """
    if datetime.now() - creation_time > timedelta(days=max_age_days):
        return False, "Password has expired. Please create a new one."
    return True, ""

def passcommon(password):
    """
    Check if a password is in the list of common passwords.
    """
    if password.lower() in passlist:
        return True, f"'{password}' is on haveibeenpwned.com website. Try a unique password."
    return False, "Not in the list of common passwords."

# --- CLI Interface ---
def main():
    parser = argparse.ArgumentParser(description="Password Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate password
    gen_parser = subparsers.add_parser("generate", help="Generate a random password")
    gen_parser.add_argument("--length", type=int, default=8, help="Password length (default: 8)")

    # Analyze password
    analyze_parser = subparsers.add_parser("analyze", help="Analyze password strength")
    analyze_parser.add_argument("password", help="Password to analyze")

    # Calculate entropy
    entropy_parser = subparsers.add_parser("entropy", help="Calculate password entropy")
    entropy_parser.add_argument("password", help="Password to calculate entropy for")

    # Estimate crack time
    crack_parser = subparsers.add_parser("cracktime", help="Estimate password crack time")
    crack_parser.add_argument("password", help="Password to estimate crack time for")
    crack_parser.add_argument("--unit", choices=["sec", "min", "hr"], default="sec", help="Time unit (sec, min, hr)")

    # Check if common
    common_parser = subparsers.add_parser("common", help="Check if password is common")
    common_parser.add_argument("password", help="Password to check")

    # Encrypt password
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a password")
    encrypt_parser.add_argument("password", help="Password to encrypt")

    # Decrypt password
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a password")
    decrypt_parser.add_argument("encrypted_password", help="Encrypted password (base64-encoded string)")
    decrypt_parser.add_argument("--keyfile", default="encryption_key.key", help="Encryption key file")

    args = parser.parse_args()

    if args.command == "generate":
        password = passgenerator(args.length)
        print(f"Generated password: {password}")

    elif args.command == "analyze":
        is_strong, feedback = passanalyzer(args.password)
        print(f"Password: {args.password}")
        print(f"Strong: {is_strong}")
        print(f"Feedback: {feedback}")

    elif args.command == "entropy":
        entropy = passentropy(args.password)
        print(f"Password entropy: {entropy} bits")

    elif args.command == "cracktime":
        crack_time = passcracktime(args.password, args.unit)
        print(f"Estimated crack time: {crack_time} {args.unit}")

    elif args.command == "common":
        is_common, message = passcommon(args.password)
        print(message)

    elif args.command == "encrypt":
        try:
            key = generatekey()
            encrypted = passencrypt(args.password, key)
            print(f"Encrypted password: {encrypted.decode()}")
        except Exception as e:
            print(f"Error: {str(e)}")

    elif args.command == "decrypt":
        try:
            key = loadkey(args.keyfile)
            decrypted = passdecrypt(args.encrypted_password.encode(), key)
            print(f"Decrypted password: {decrypted}")
        except Exception as e:
            print(f"Error: {str(e)}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()