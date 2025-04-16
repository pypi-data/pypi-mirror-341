"""
암호화된 모듈을 임포트하기 위한 후크를 구현하는 모듈
"""

from typing import Optional, Any, Dict, Set
import sys
import os
import importlib.machinery
import importlib.util
from .crypto import CryptoManager

class EncryptedImporter:
    """암호화된 모듈을 임포트하는 클래스"""
    
    def __init__(self, crypto_manager: CryptoManager, base_dir: str):
        """초기화
        
        Args:
            crypto_manager (CryptoManager): 암호화/복호화를 담당하는 매니저
            base_dir (str): 암호화된 모듈들이 있는 기본 디렉토리
        """
        self.crypto_manager = crypto_manager
        self.base_dir = base_dir
        self.cache: Dict[str, Any] = {}
        self.loading: Set[str] = set()
    
    def find_spec(self, fullname: str, path: Optional[Any] = None, target: Optional[Any] = None) -> Optional[Any]:
        """모듈 사양을 찾습니다.
        
        Args:
            fullname (str): 모듈의 전체 이름
            path (Optional[Any]): 검색 경로
            target (Optional[Any]): 대상 모듈
            
        Returns:
            Optional[Any]: 모듈 사양 또는 None
        """
        if fullname in sys.modules:
            return None
        
        # 모듈 이름을 파일 경로로 변환
        module_path = fullname.replace('.', os.sep)
        
        # 일반 모듈 파일 확인
        module_file = os.path.join(self.base_dir, module_path + '.py.enc')
        if os.path.exists(module_file):
            return self._create_spec(fullname, module_file, False)
        
        # 패키지 확인
        package_init = os.path.join(self.base_dir, module_path, '__init__.py.enc')
        if os.path.exists(package_init):
            return self._create_spec(fullname, package_init, True)
        
        return None
    
    def _create_spec(self, name: str, origin: str, is_package: bool) -> Any:
        """모듈 사양을 생성합니다.
        
        Args:
            name (str): 모듈 이름
            origin (str): 모듈 파일 경로
            is_package (bool): 패키지 여부
            
        Returns:
            Any: 모듈 사양
        """
        spec = importlib.machinery.ModuleSpec(name, self, is_package=is_package)
        spec.origin = origin
        spec.has_location = True
        if is_package:
            spec.submodule_search_locations = [os.path.dirname(origin)]
        return spec
    
    def create_module(self, spec: Any) -> Any:
        """모듈을 생성합니다.
        
        Args:
            spec (Any): 모듈 사양
            
        Returns:
            Any: 생성된 모듈
        """
        return None  # importlib.util.module_from_spec 사용
    
    def exec_module(self, module: Any) -> None:
        """모듈을 실행합니다.
        
        Args:
            module (Any): 실행할 모듈
        """
        name = module.__name__
        if name in self.loading:
            return
        
        self.loading.add(name)
        try:
            # 암호화된 파일을 복호화
            with open(module.__spec__.origin, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.crypto_manager.decrypt_file(module.__spec__.origin)
            
            # 복호화된 코드를 컴파일하고 실행
            code = compile(decrypted_data, module.__spec__.origin, 'exec')
            exec(code, module.__dict__)
        finally:
            self.loading.remove(name)

def install_importer(crypto_manager: CryptoManager, base_dir: str) -> None:
    """암호화된 모듈 임포트 후크를 설치합니다.
    
    Args:
        crypto_manager (CryptoManager): 암호화/복호화를 담당하는 매니저
        base_dir (str): 암호화된 모듈들이 있는 기본 디렉토리
    """
    importer = EncryptedImporter(crypto_manager, base_dir)
    sys.meta_path.insert(0, importer) 