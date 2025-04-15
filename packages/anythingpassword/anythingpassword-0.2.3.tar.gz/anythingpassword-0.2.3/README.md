# AnythingPassword  
**Password Management and Encryption Application**

## Overview

This Python application provides a suite of tools for generating, analyzing, encrypting, and managing passwords securely. It includes functionality to generate strong random passwords, evaluate password strength, calculate password entropy and crack time, check for password expiration, and detect common passwords. Additionally, it supports secure password encryption and decryption using the Fernet symmetric encryption algorithm, with the encryption key stored securely in the same directory as the script.

The application is designed to be modular, secure, and user-friendly, with robust error handling and platform compatibility (Unix-like systems and Windows).

---

## ✨ Features

### 🔑 Password Generation
- Generates random passwords of specified length using a mix of lowercase, uppercase, digits, and special characters.
- Default length is 8 characters if not specified.

### 🛡️ Password Strength Analysis
- Evaluates passwords based on length, character types (uppercase, lowercase, digits, special characters), and commonality.
- Provides feedback and a strong password suggestion if the input password is weak.
- Checks against a list of common passwords.

### 📊 Password Security Metrics
- Calculates password entropy (in bits) to measure randomness.
- Estimates the time required to crack a password via brute force in seconds, minutes, or hours.
- Checks if a password has expired based on a creation timestamp and maximum age (default 90 days).

### 🔐 Password Encryption/Decryption
- Encrypts passwords using a securely generated Fernet key.
- Decrypts encrypted passwords using the same key.
- Stores the encryption key securely in the script’s directory with restricted permissions.

### 🗝️ Key Management
- Generates and saves a Fernet key to a file (`encryption_key.key`) in the script’s directory.
- Loads the key from the file for encryption/decryption.
- Ensures secure file permissions (owner-only read/write on Unix-like systems).

---

## 📦 Installation

```bash
pip install anythingpassword

## Sample Usage
from anythingpassword import (
    generatekey,
    loadkey,
    passencrypt,
    passdecrypt,
    passgenerator,
    passanalyzer,
    passentropy,
    passcracktime,
    passexpiration,
    passcommon
)
from datetime import datetime, timedelta

# Generate and save a new encryption key
key = generatekey()
print("Encryption key generated and saved.")

# Load the encryption key
loaded_key = loadkey()
print("Encryption key loaded.")

# Generate a random password
password = passgenerator(12)
print(f"Generated Password: {password}")

# Analyze password strength
is_strong, feedback = passanalyzer(password)
print("Strength Check:")
print(feedback)

# Calculate password entropy
entropy = passentropy(password)
print(f"Password Entropy: {entropy} bits")

# Estimate crack time
crack_time_sec = passcracktime(password, unit='sec')
print(f"Estimated Crack Time: {crack_time_sec} seconds")

# Encrypt the password
encrypted_pass = passencrypt(password, loaded_key)
print(f"Encrypted Password: {encrypted_pass}")

# Decrypt the password
decrypted_pass = passdecrypt(encrypted_pass, loaded_key)
print(f"Decrypted Password: {decrypted_pass}")

# Check if the password is expired (e.g. created 100 days ago)
creation_time = datetime.now() - timedelta(days=100)
expired, status = passexpiration(creation_time)
print(f"Expiration Check: {status}")

# Check if the password is common (e.g. in known data breaches)
is_common, msg = passcommon(password)
print(f"Common Password Check: {msg}")