import hashlib
import base64
import secrets
import string
import random
from typing import Union

class CryptoX:
    def __init__(self):
        self.charset = string.ascii_letters + string.digits + string.punctuation
    
    # 🔐 HASHING
    def md5(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()
    
    def sha1(self, data: str) -> str:
        return hashlib.sha1(data.encode()).hexdigest()
    
    def sha256(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    def sha512(self, data: str) -> str:
        return hashlib.sha512(data.encode()).hexdigest()
    
    def blake2b(self, data: str) -> str:
        return hashlib.blake2b(data.encode()).hexdigest()
    
    def hash_all(self, data: str) -> dict:
        return {
            'md5': self.md5(data),
            'sha1': self.sha1(data),
            'sha256': self.sha256(data),
            'sha512': self.sha512(data),
            'blake2b': self.blake2b(data)
        }
    
    # 🔄 BASE64
    def base64_encode(self, data: str) -> str:
        return base64.b64encode(data.encode()).decode()
    
    def base64_decode(self, data: str) -> str:
        return base64.b64decode(data.encode()).decode()
    
    def base64_url_encode(self, data: str) -> str:
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')
    
    def base64_url_decode(self, data: str) -> str:
        padding = 4 - (len(data) % 4)
        data = data + ('=' * padding)
        return base64.urlsafe_b64decode(data.encode()).decode()
    
    # 🎲 RANDOM
    def random_string(self, length: int = 32) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def random_hex(self, length: int = 32) -> str:
        return secrets.token_hex(length // 2)
    
    def random_bytes(self, length: int = 32) -> bytes:
        return secrets.token_bytes(length)
    
    def uuid(self) -> str:
        import uuid
        return str(uuid.uuid4())
    
    # 🔑 PASSWORD HASHING
    def password_hash(self, password: str, salt: str = None, iterations: int = 100000) -> dict:
        if salt is None:
            salt = self.random_string(16)
        
        # PBKDF2
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            iterations
        ).hex()
        
        return {
            'hash': key,
            'salt': salt,
            'iterations': iterations,
            'algorithm': 'pbkdf2_sha256'
        }
    
    def password_verify(self, password: str, hash_dict: dict) -> bool:
        new_hash = self.password_hash(password, hash_dict['salt'], hash_dict['iterations'])
        return new_hash['hash'] == hash_dict['hash']
    
    # ✨ SIMPLE ENCRYPTION
    def caesar_cipher(self, text: str, shift: int) -> str:
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def xor_encrypt(self, data: str, key: str) -> str:
        encrypted = []
        key_bytes = key.encode()
        for i, char in enumerate(data):
            encrypted_char = ord(char) ^ key_bytes[i % len(key_bytes)]
            encrypted.append(chr(encrypted_char))
        return ''.join(encrypted)
    
    def xor_decrypt(self, data: str, key: str) -> str:
        return self.xor_encrypt(data, key)  # XOR es simétrico
    
    # 📊 UTILITIES
    def entropy(self, data: str) -> float:
        """Calcula la entropía de Shannon"""
        from math import log2
        entropy = 0
        for x in range(256):
            p_x = data.count(chr(x)) / len(data)
            if p_x > 0:
                entropy += -p_x * log2(p_x)
        return entropy
    
    def strength_score(self, password: str) -> int:
        score = 0
        
        if len(password) >= 8: score += 20
        if len(password) >= 12: score += 20
        if len(password) >= 16: score += 10
        
        if any(c.islower() for c in password): score += 10
        if any(c.isupper() for c in password): score += 10
        if any(c.isdigit() for c in password): score += 10
        if any(c in string.punctuation for c in password): score += 10
        
        entropy_val = self.entropy(password)
        if entropy_val > 3: score += 10
        if entropy_val > 4: score += 10
        
        return min(score, 100)
    
    def password_generator(self, length: int = 12, use_special: bool = True) -> str:
        chars = string.ascii_letters + string.digits
        if use_special:
            chars += string.punctuation
        
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                (not use_special or any(c in string.punctuation for c in password))):
                return password
    
    # 🔍 ANALYSIS
    def hash_identifier(self, hash_str: str) -> list:
        """Identifica tipo de hash"""
        hash_len = len(hash_str)
        patterns = []
        
        if hash_len == 32: patterns.append("MD5")
        if hash_len == 40: patterns.append("SHA-1")
        if hash_len == 64: patterns.append("SHA-256")
        if hash_len == 128: patterns.append("SHA-512")
        if hash_len == 96: patterns.append("BLAKE2b")
        if hash_len == 56: patterns.append("SHA-224")
        if hash_len == 112: patterns.append("SHA-384")
        
        return patterns if patterns else ["Unknown"]
    
    def is_hash(self, data: str) -> bool:
        """Verifica si una cadena parece ser un hash"""
        return len(self.hash_identifier(data)) > 0

# Funciones rápidas CORREGIDAS
def md5(data): return CryptoX().md5(data)
def sha1(data): return CryptoX().sha1(data)
def sha256(data): return CryptoX().sha256(data)
def sha512(data): return CryptoX().sha512(data)
def base64_encode(data): return CryptoX().base64_encode(data)
def base64_decode(data): return CryptoX().base64_decode(data)
def random_string(length=32): return CryptoX().random_string(length)
def random_hex(length=32): return CryptoX().random_hex(length)
def password_generator(length=12): return CryptoX().password_generator(length)
