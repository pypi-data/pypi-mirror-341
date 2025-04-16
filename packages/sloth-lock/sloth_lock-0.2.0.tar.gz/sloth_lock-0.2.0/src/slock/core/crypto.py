"""
암호화/복호화 핵심 로직을 담당하는 모듈
"""

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class CryptoManager:
    """암호화/복호화를 관리하는 클래스"""
    
    def __init__(self, password: str):
        """초기화
        
        Args:
            password (str): 암호화/복호화에 사용할 비밀번호
        """
        self.key = self._generate_key(password)
        self.fernet = Fernet(self.key)
    
    def _generate_key(self, password: str) -> bytes:
        """비밀번호를 사용하여 암호화 키를 생성합니다.
        
        Args:
            password (str): 비밀번호
            
        Returns:
            bytes: 생성된 암호화 키
        """
        salt = b'static_salt_for_key_generation'  # 실제 사용 시에는 랜덤한 salt를 사용하는 것이 좋습니다
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_file(self, input_path: str, output_path: str) -> None:
        """파일을 암호화합니다.
        
        Args:
            input_path (str): 암호화할 파일 경로
            output_path (str): 암호화된 파일을 저장할 경로
        """
        with open(input_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = self.fernet.encrypt(file_data)
        
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
    
    def decrypt_file(self, input_path: str) -> bytes:
        """암호화된 파일을 복호화합니다.
        
        Args:
            input_path (str): 복호화할 파일 경로
            
        Returns:
            bytes: 복호화된 데이터
        """
        with open(input_path, 'rb') as file:
            encrypted_data = file.read()
        
        return self.fernet.decrypt(encrypted_data)
    
    def encrypt_directory(self, input_dir: str, output_dir: str) -> None:
        """디렉토리의 모든 Python 파일을 암호화합니다.
        
        Args:
            input_dir (str): 암호화할 디렉토리 경로
            output_dir (str): 암호화된 파일들을 저장할 디렉토리 경로
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.py'):
                    input_path = os.path.join(root, file)
                    rel_path = os.path.relpath(input_path, input_dir)
                    output_path = os.path.join(output_dir, rel_path + '.enc')
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    self.encrypt_file(input_path, output_path) 