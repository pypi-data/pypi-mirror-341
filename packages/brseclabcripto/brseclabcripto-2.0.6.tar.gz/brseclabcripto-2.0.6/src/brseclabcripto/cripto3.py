"""
Functions for AES256-GCM encryption/decryption (pyca/cryptography and gpg) and Argon2 hashing.
This module provides functions to generate an AES key, encrypt and decrypt messages,
and hash and verify passwords using Argon2 and SHA3-256.
It uses the criptography library for AES encryption and Argon2 for password hashing.
It is important to note that the AES key should be kept secret and secure.
The Argon2 hash should also be stored securely, as it is used to verify passwords.
This module is intended for educational purposes and should not be used in
production without proper security measures.

Author: RAFAEL PERAZZO B MOTA
Date: 2025-03-30
Version: 1.1
"""

import base64
import secrets
import cryptography
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import argon2
from argon2 import PasswordHasher

class SecCripto:
    """
    Class for AES256-GCM encryption/decryption and Argon2 hashing.
    """

    def __init__(self,key):
        """
        Initializes the SecCripto class with a given AES key.
        :param key: AES key (must be 16, 24, or 32 bytes long) - bytes or str
        """
        if isinstance(key, str):
            # Convert hexadecimal string key to bytes
            try:
                self.key = bytes.fromhex(key)
            except ValueError as exc:
                # If the key is not a valid hexadecimal string, raise an error
                raise ValueError(
                    "Invalid key format. Key must be a hexadecimal string."
                ) from exc
        elif isinstance(key, bytes):
            # If the key is already in bytes, just assign it
            self.key = key
        else:
            # If the key is neither a string nor bytes, raise an error
            raise TypeError("Key must be a hexadecimal string or bytes.")
        # Check if the key length is valid (16, 24, or 32 bytes)
        if len(self.key) not in (16, 24, 32):
            raise ValueError(
                "Invalid key length. Key must be 16, 24, or 32 bytes long."
            )

    def aes_gcm_encrypt(self,plaintext):
        """
        Encrypts the plaintext using AES GCM encryption with a random nonce.
        :param plaintext: plaintext to be encrypted - bytes
        :return: ciphertext (nonce + ciphertext + tag) - base64 string
        """
        if isinstance(plaintext, str):
            # Convert string plaintext to bytes
            plaintext = plaintext.encode()
        cipher = AESGCM(self.key)
        nonce = secrets.token_bytes(12)  # Generate a random nonce
        ciphertext = cipher.encrypt(nonce, plaintext, None)
        return base64.b64encode(nonce + ciphertext).decode("utf-8")

    def aes_gcm_decrypt(self,ciphertext):
        """
        Decrypts the ciphertext using AES GCM decryption.
        :param ciphertext: ciphertext to be decrypted (nonce + ciphertext + tag)
        - bytes or base64 string
        :return: decrypted plaintext - string
        """
        if isinstance(ciphertext, str):
            # Convert base64 string ciphertext to bytes
            ciphertext = base64.b64decode(ciphertext)
        nonce = ciphertext[:12]
        ciphertext = ciphertext[12:]
        cipher = AESGCM(self.key)
        plaintext = cipher.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")
    
    def hash_hmac(self,message):
        """
        Computes the HMAC of the given message using the provided key.
        :param message: message to be hashed - bytes
        :return: HMAC - hexadecimal string
        """
        if isinstance(message, str):
            # Convert string message to bytes
            message = message.encode()
        h = hmac.HMAC(self.key, hashes.SHA3_256())
        h.update(message)
        return h.finalize().hex()

    def hash_hmac_verify(self, message, hmac_value):
        """
        Verifies the HMAC of the given message using the provided key.
        :param message: message to be hashed - bytes or string
        :param hmac_value: HMAC to be verified - bytes or hexadecimal string
        :return: True if the HMAC is valid, False otherwise
        """
        if isinstance(message, str):
            # Convert string message to bytes
            message = message.encode()
        if isinstance(hmac_value, str):
            # Convert hexadecimal string HMAC to bytes
            try:
                hmac_value = bytes.fromhex(hmac_value)
            except ValueError:
                # If the HMAC is not a valid hexadecimal string, return False
                return False
        h = hmac.HMAC(self.key, hashes.SHA3_256())
        h.update(message)
        try:
            h.verify(hmac_value)
            return True
        except cryptography.exceptions.InvalidSignature:
            return False
        
    def hash_argon2id(self, password):
        """
        Applies Argon2 hashing to the password using a HMAC.
        :param password: password to be hashed - string
        :return: Argon2 hash - string
        """
        if isinstance(password, str):
            # Convert string password to bytes
            password = password.encode()
        # Create the HMAC
        signature = self.hash_hmac(password)
        # Apply Argon2 hashing
        ph = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            salt_len=16,
            encoding="utf-8",
        )
        hash_argon = ph.hash(signature)
        return hash_argon

    def hash_argon2id_verify(self,hash_argon, password):
        """
        Verifies if the Argon2 hash matches the password.
        :param hash_argon: stored Argon2 hash - string
        :param password: password to be verified - string
        :return: True if the password is correct, False otherwise
        """
        if isinstance(password, str):
            # Convert string password to bytes
            password = password.encode()
        # Create the HMAC
        signature = self.hash_hmac(password)
        # Apply Argon2 hashing
        ph = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            salt_len=16,
            encoding="utf-8",
        )
        try:
            ph.verify(hash_argon, signature)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        
    def sha256(self,message):
        """
        Computes the SHA3-256 hash of the given message.
        :param message: message to be hashed - bytes or string
        :return: SHA3-256 hash - hexadecimal string
        """
        if isinstance(message, str):
            # Convert string message to bytes
            message = message.encode()
        digest = hashes.Hash(hashes.SHA3_256())
        digest.update(message)
        return digest.finalize().hex()

    def sha256_verify(self,message, hash_value):
        """
        Verifies if the SHA3-256 hash matches the message.
        :param message: message to be verified - bytes or string
        :param hash_value: SHA3-256 hash to be verified - bytes or hexadecimal string
        :return: True if the hash is valid, False otherwise
        """
        if isinstance(message, str):
            # Convert string message to bytes
            message = message.encode()
        if isinstance(hash_value, str):
            # Convert hexadecimal string hash to bytes
            try:
                hash_value = bytes.fromhex(hash_value)
            except ValueError:
                # If the hash is not a valid hexadecimal string, return False
                return False
        digest = hashes.Hash(hashes.SHA3_256())
        digest.update(message)
        return digest.finalize() == hash_value
    
    def generate_aes_key(self,length):
        """
        Generates a random AES key.
        length: length of the key in bytes (must be 16, 24, or 32)
        :return: AES key - hexadecimal string
        """
        if length not in (16, 24, 32):
            raise ValueError("Key length must be 16, 24, or 32 bytes.")
        return secrets.token_bytes(length).hex()
