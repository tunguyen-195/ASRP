#!/usr/bin/env python3
"""
generate_secret.py

Tạo và in ra một SECRET_KEY ngẫu nhiên để dùng cho Flask.
"""

import secrets

def main():
    # Tạo key 32 byte (64 hex) - đủ mạnh cho SECRET_KEY
    secret_key = secrets.token_hex(32)  
    print("SECRET_KEY =", secret_key)

if __name__ == "__main__":
    main()

# SECRET_KEY = b13eff07110a432a03e3731c2633a6b8a6ee8152fd2af5dd8b0438b2b3dd983d