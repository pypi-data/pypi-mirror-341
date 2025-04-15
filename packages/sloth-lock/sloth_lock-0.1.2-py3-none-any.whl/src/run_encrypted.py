"""
암호화된 Python 파일을 실행하는 스크립트
"""

import sys
import importlib.util
import os
import tempfile

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cli import decrypt_file

def run_encrypted_python(encrypted_file: str, password: str) -> None:
    """
    암호화된 Python 파일을 메모리에서 복호화하여 실행합니다.
    """
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        # 파일 복호화
        decrypt_file(encrypted_file, temp_path, password)
        
        # 모듈로 임포트
        spec = importlib.util.spec_from_file_location("encrypted_module", temp_path)
        if spec is None or spec.loader is None:
            raise ImportError("모듈을 로드할 수 없습니다.")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules["encrypted_module"] = module
        spec.loader.exec_module(module)
        
    finally:
        # 임시 파일 삭제
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def main():
    if len(sys.argv) != 3:
        print("사용법: python run_encrypted.py <암호화된_파일> <비밀번호>")
        sys.exit(1)
    
    encrypted_file = sys.argv[1]
    password = sys.argv[2]
    
    try:
        run_encrypted_python(encrypted_file, password)
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 