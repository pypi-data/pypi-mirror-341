import os
import tempfile
import pytest
from src.cli import generate_key, encrypt_file, decrypt_file

def test_generate_key():
    """키 생성 테스트"""
    password = "test_password"
    key = generate_key(password)
    assert len(key) == 44  # Fernet 키는 44바이트 길이
    assert isinstance(key, bytes)

def test_encrypt_decrypt():
    """암호화 및 복호화 테스트"""
    # 테스트용 임시 파일 생성
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(b"Hello, World!")
        temp_input_path = temp_input.name

    temp_encrypted = temp_input_path + ".enc"
    temp_decrypted = temp_input_path + ".dec"

    try:
        # 암호화
        password = "test_password"
        encrypt_file(temp_input_path, temp_encrypted, password)
        assert os.path.exists(temp_encrypted)
        assert os.path.getsize(temp_encrypted) > 0

        # 복호화
        decrypt_file(temp_encrypted, temp_decrypted, password)
        assert os.path.exists(temp_decrypted)
        
        # 원본과 복호화된 내용 비교
        with open(temp_decrypted, 'rb') as f:
            decrypted_content = f.read()
        assert decrypted_content == b"Hello, World!"

    finally:
        # 임시 파일 정리
        for file_path in [temp_input_path, temp_encrypted, temp_decrypted]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_decrypt_wrong_password():
    """잘못된 비밀번호로 복호화 시도 테스트"""
    # 테스트용 임시 파일 생성
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(b"Hello, World!")
        temp_input_path = temp_input.name

    temp_encrypted = temp_input_path + ".enc"
    temp_decrypted = temp_input_path + ".dec"

    try:
        # 암호화
        password = "correct_password"
        encrypt_file(temp_input_path, temp_encrypted, password)

        # 잘못된 비밀번호로 복호화 시도
        with pytest.raises(Exception):
            decrypt_file(temp_encrypted, temp_decrypted, "wrong_password")

    finally:
        # 임시 파일 정리
        for file_path in [temp_input_path, temp_encrypted, temp_decrypted]:
            if os.path.exists(file_path):
                os.unlink(file_path) 