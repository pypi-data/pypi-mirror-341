"""
명령줄 인터페이스를 구현하는 모듈
"""

import os
import sys
import click
import importlib
import runpy
import shutil
from pathlib import Path
from typing import Optional
from ..core.crypto import CryptoManager
from ..core.dependency import DependencyAnalyzer
from ..core.importer import install_importer

class SlockError(Exception):
    """Slock 관련 예외의 기본 클래스"""
    pass

class FileSystemError(SlockError):
    """파일 시스템 관련 예외"""
    pass

class EncryptionError(SlockError):
    """암호화 관련 예외"""
    pass

class ModuleError(SlockError):
    """모듈 관련 예외"""
    pass

def _validate_path(path: str, should_exist: bool = True) -> None:
    """경로의 유효성을 검사합니다.
    
    Args:
        path (str): 검사할 경로
        should_exist (bool): 경로가 존재해야 하는지 여부
        
    Raises:
        FileSystemError: 경로가 유효하지 않은 경우
    """
    try:
        path_obj = Path(path)
        if should_exist and not path_obj.exists():
            raise FileSystemError(f"경로가 존재하지 않습니다: {path}")
        if not should_exist and path_obj.exists():
            raise FileSystemError(f"경로가 이미 존재합니다: {path}")
    except Exception as e:
        raise FileSystemError(f"잘못된 경로입니다: {path}") from e

def _ensure_package_structure(input_dir: str) -> None:
    """디렉토리가 Python 패키지 구조를 가지도록 보장합니다.
    
    Args:
        input_dir (str): 확인할 디렉토리 경로
        
    Raises:
        FileSystemError: 패키지 구조 생성 실패
    """
    def _create_init_file(dir_path: str) -> None:
        """__init__.py 파일을 생성하거나 확인합니다.
        
        Args:
            dir_path (str): 디렉토리 경로
            
        Raises:
            FileSystemError: 파일 생성 실패
        """
        try:
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('"""\nsloth-lock init generation\n"""\n')
        except Exception as e:
            raise FileSystemError(f"__init__.py 파일 생성 실패: {dir_path}") from e
    
    try:
        # 현재 디렉토리 확인
        _create_init_file(input_dir)
        
        # 하위 디렉토리들도 확인
        for root, dirs, _ in os.walk(input_dir):
            for dir_name in dirs:
                if dir_name.startswith('.'):  # 숨김 디렉토리는 건너뜀
                    continue
                dir_path = os.path.join(root, dir_name)
                _create_init_file(dir_path)
    except Exception as e:
        raise FileSystemError(f"패키지 구조 생성 실패: {input_dir}") from e

@click.group()
def cli():
    """Sloth-Lock: 파일 암호화/복호화 도구"""
    pass

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.argument('password')
def encrypt(input_file: str, output_file: str, password: str):
    """파일을 암호화합니다."""
    try:
        _validate_path(input_file)
        _validate_path(output_file, should_exist=False)
        
        crypto = CryptoManager(password)
        crypto.encrypt_file(input_file, output_file)
        click.echo(f"파일이 암호화되어 {output_file}에 저장되었습니다.")
    except SlockError as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"예상치 못한 오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.argument('password')
def decrypt(input_file: str, output_file: str, password: str):
    """암호화된 파일을 복호화합니다."""
    try:
        _validate_path(input_file)
        _validate_path(output_file, should_exist=False)
        
        crypto = CryptoManager(password)
        decrypted_data = crypto.decrypt_file(input_file)
        
        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
        
        click.echo(f"파일이 복호화되어 {output_file}에 저장되었습니다.")
    except SlockError as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"예상치 못한 오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('input_dir')
@click.argument('output_dir')
@click.argument('password')
def encrypt_dir(input_dir: str, output_dir: str, password: str):
    """디렉토리의 모든 Python 파일을 암호화합니다."""
    try:
        _validate_path(input_dir)
        _validate_path(output_dir, should_exist=False)
        
        # 패키지 구조 확인 및 생성
        _ensure_package_structure(input_dir)
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        crypto = CryptoManager(password)
        crypto.encrypt_directory(input_dir, output_dir)
        click.echo(f"디렉토리가 암호화되어 {output_dir}에 저장되었습니다.")
    except SlockError as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"예상치 못한 오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('encrypted_dir')
@click.argument('password')
@click.argument('main_module')
def run_dir(encrypted_dir: str, password: str, main_module: str):
    """암호화된 디렉토리의 Python 모듈을 실행합니다."""
    try:
        _validate_path(encrypted_dir)
        
        # Python 경로에 디렉토리 추가
        encrypted_dir_abs = os.path.abspath(encrypted_dir)
        sys.path.insert(0, encrypted_dir_abs)
        
        # 암호화/복호화 매니저 초기화
        crypto = CryptoManager(password)
        
        # 임포트 후크 설치
        install_importer(crypto, encrypted_dir_abs)
        
        # 의존성 분석
        analyzer = DependencyAnalyzer(encrypted_dir_abs)
        analyzer.build_graph()
        
        # 메인 모듈 실행
        try:
            module = importlib.import_module(main_module)
            if hasattr(module, 'main'):
                module.main()
            else:
                # main 함수가 없는 경우 모듈 전체를 실행
                runpy.run_module(main_module, run_name='__main__')
        except ImportError as e:
            raise ModuleError(f"모듈을 찾을 수 없습니다: {main_module}") from e
        except Exception as e:
            raise ModuleError(f"모듈 실행 중 오류가 발생했습니다: {str(e)}") from e
            
    except SlockError as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"예상치 못한 오류가 발생했습니다: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli() 