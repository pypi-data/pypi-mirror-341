import random
import string
import re
import math
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from .passwordlist import passlist


def save_key_securely(key, filename="encryption_key.key"):
    """
    Save the encryption key to a file in the same directory with restricted permissions.
    """
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, filename)
        
        # Write the key to the file
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        
        # Set file permissions to read/write for owner only (Unix-like systems)
        if os.name != 'nt':  # Not Windows
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
    
    # Define character sets
    characters = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        string.punctuation
    )
    
    # Generate password
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
    
    # Check length
    if len(password) < 8:
        feedback.append("Password should be at least 8 characters long.")
        is_strong = False
    
    # Check for uppercase letters
    if not re.search(r'[A-Z]', password):
        feedback.append("Add at least one uppercase letter.")
        is_strong = False
    
    # Check for lowercase letters
    if not re.search(r'[a-z]', password):
        feedback.append("Add at least one lowercase letter.")
        is_strong = False
    
    # Check for digits
    if not re.search(r'\d', password):
        feedback.append("Add at least one number.")
        is_strong = False
    
    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append("Add at least one special character (e.g., !@#$).")
        is_strong = False

    # Check for common password
    if (passcommon(password)[0] == True):
        feedback = []
        feedback.append("Password is found on haveibeenpwned website")
        is_strong = False
    
    # Generate hint if password is weak
    if not is_strong:
        hint = passgenerator(12)  # Generate a strong password as a hint
        feedback.append(f"Here's a strong password suggestion: {hint}")
    
    return is_strong, "\n".join(feedback) if feedback else "Password is strong!"


def passentropy(password):
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

def passcracktime(password, unit = 'sec'):
    char_set_size = len(set(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation))
    attempts = char_set_size ** len(password)
    seconds = attempts / 1_000_000_000  # 1B attempts per second
    if unit.lower() == 'sec':
        return round(seconds, 2)  # Already in seconds
    elif unit.lower() == 'min':
        return round(seconds/60, 2)  # Convert minutes to seconds
    elif unit.lower() == 'hr':
        return round(seconds/3600, 2)  # Convert hours to seconds
    else:
        return "Invalid unit: Use 'sec', 'min', or 'hr'."
    
def passexpiration(creation_time, max_age_days=90):
    if datetime.now() - creation_time > timedelta(days=max_age_days):
        return False, "Password has expired. Please create a new one."
    return True, "Password is active"


# common_passwords = {"password", "123456", "qwerty"}  # Example set
def passcommon(password):
    if password.lower() in passlist:
        return True, f"'{password}' is on haveibeenpwned.com website. Try a unique password."
    return False, "Not in the list of common password"


