"""
의존성 분석을 담당하는 모듈
"""

import os
import ast
from typing import Dict, List, Set
import astroid

class DependencyAnalyzer:
    """Python 모듈의 의존성을 분석하는 클래스"""
    
    def __init__(self, base_dir: str):
        """초기화
        
        Args:
            base_dir (str): 분석할 디렉토리의 기본 경로
        """
        self.base_dir = base_dir
        self.dependency_graph: Dict[str, Set[str]] = {}
    
    def analyze_file(self, file_path: str) -> Set[str]:
        """파일의 의존성을 분석합니다.
        
        Args:
            file_path (str): 분석할 파일 경로
            
        Returns:
            Set[str]: 의존하는 모듈들의 집합
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        try:
            tree = astroid.parse(content)
            imports = set()
            
            for node in astroid.walk(tree):
                if isinstance(node, astroid.Import):
                    for name, _ in node.names:
                        imports.add(name)
                elif isinstance(node, astroid.ImportFrom):
                    if node.module:
                        imports.add(node.module)
            
            return imports
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {str(e)}")
            return set()
    
    def build_graph(self) -> None:
        """디렉토리의 모든 Python 파일에 대한 의존성 그래프를 구축합니다."""
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.base_dir)
                    module_name = rel_path.replace('/', '.').replace('\\', '.')[:-3]
                    
                    self.dependency_graph[module_name] = self.analyze_file(file_path)
    
    def get_dependencies(self, module_name: str) -> List[str]:
        """모듈의 모든 의존성을 재귀적으로 찾습니다.
        
        Args:
            module_name (str): 분석할 모듈 이름
            
        Returns:
            List[str]: 의존하는 모든 모듈들의 리스트 (순서대로)
        """
        visited = set()
        result = []
        
        def visit(name: str) -> None:
            if name in visited:
                return
            
            visited.add(name)
            
            for dep in self.dependency_graph.get(name, set()):
                if dep in self.dependency_graph:
                    visit(dep)
            
            result.append(name)
        
        visit(module_name)
        return result 