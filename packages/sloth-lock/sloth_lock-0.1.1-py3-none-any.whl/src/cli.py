"""
파일 암호화/복호화 명령줄 인터페이스
"""

import argparse
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import cryptography
import sys

def generate_key(password: str) -> bytes:
    """비밀번호를 사용하여 암호화 키를 생성합니다."""
    salt = b'static_salt_for_key_generation'  # 실제 사용 시에는 랜덤한 salt를 사용하는 것이 좋습니다
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(input_file: str, output_file: str, password: str) -> None:
    """파일을 암호화하여 저장합니다."""
    key = generate_key(password)
    f = Fernet(key)
    
    with open(input_file, 'rb') as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(input_file: str, output_file: str, password: str) -> None:
    """암호화된 파일을 복호화하여 저장합니다."""
    key = generate_key(password)
    f = Fernet(key)
    
    with open(input_file, 'rb') as file:
        encrypted_data = file.read()
    
    decrypted_data = f.decrypt(encrypted_data)
    with open(output_file, 'wb') as file:
        file.write(decrypted_data)

def main():
    parser = argparse.ArgumentParser(description='파일 암호화/복호화 도구')
    subparsers = parser.add_subparsers(dest='command', help='명령어')
    
    # 암호화 명령어
    encrypt_parser = subparsers.add_parser('encrypt', help='파일 암호화')
    encrypt_parser.add_argument('input_file', help='암호화할 입력 파일 경로')
    encrypt_parser.add_argument('output_file', help='암호화된 파일을 저장할 경로')
    encrypt_parser.add_argument('password', help='암호화에 사용할 비밀번호')
    
    # 복호화 명령어
    decrypt_parser = subparsers.add_parser('decrypt', help='파일 복호화')
    decrypt_parser.add_argument('input_file', help='복호화할 입력 파일 경로')
    decrypt_parser.add_argument('output_file', help='복호화된 파일을 저장할 경로')
    decrypt_parser.add_argument('password', help='복호화에 사용할 비밀번호')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'encrypt':
            encrypt_file(args.input_file, args.output_file, args.password)
            print(f"파일이 암호화되어 {args.output_file}에 저장되었습니다.")
        elif args.command == 'decrypt':
            decrypt_file(args.input_file, args.output_file, args.password)
            print(f"파일이 복호화되어 {args.output_file}에 저장되었습니다.")
        else:
            parser.print_help()
    except cryptography.fernet.InvalidToken:
        print("\n[오류] 복호화에 실패했습니다.")
        print("원인: 잘못된 비밀번호를 입력하셨습니다.")
        print("해결 방법: 암호화할 때 사용한 비밀번호를 정확히 입력해주세요.")
        sys.exit(1)
    except FileNotFoundError:
        print("\n[오류] 파일을 찾을 수 없습니다.")
        print(f"입력 파일 경로: {args.input_file}")
        print("해결 방법: 파일 경로가 올바른지 확인해주세요.")
        sys.exit(1)
    except Exception as e:
        print("\n[오류] 예상치 못한 오류가 발생했습니다.")
        print(f"상세 내용: {str(e)}")
        print("해결 방법: 입력값을 다시 확인해주세요.")
        sys.exit(1)

if __name__ == '__main__':
    main() 