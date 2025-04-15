# Sloth-Lock (파이썬 파일 암호화 도구)

This tool provides secure file encryption and decryption capabilities, with special support for executing encrypted Python files.

이 도구는 안전한 파일 암호화/복호화 기능을 제공하며, 특히 암호화된 Python 파일을 실행할 수 있는 기능을 지원합니다.

## Features (기능)

- File encryption and decryption using Fernet (symmetric encryption)
- Secure password-based key generation
- Direct execution of encrypted Python files
- User-friendly error messages
- Command-line interface

- Fernet(대칭 암호화)를 사용한 파일 암호화/복호화
- 비밀번호 기반의 안전한 키 생성
- 암호화된 Python 파일 직접 실행
- 사용자 친화적인 오류 메시지
- 명령줄 인터페이스

## Installation (설치 방법)

```bash
pip install sloth-lock
```

## Usage (사용 방법)

### File Encryption (파일 암호화)

```bash
# Command format (명령어 형식)
slock-enc <input_file> <output_file> <password>

# Example (예시)
slock-enc secret.txt secret.txt.enc "my_secure_password"
```

### File Decryption (파일 복호화)

```bash
# Command format (명령어 형식)
slock-dec <input_file> <output_file> <password>

# Example (예시)
slock-dec secret.txt.enc secret_decrypted.txt "my_secure_password"
```

### Running Encrypted Python Files (암호화된 Python 파일 실행)

```bash
# Command format (명령어 형식)
slock-run <encrypted_file> <password>

# Example (예시)
slock-run script.py.enc "my_secure_password"
```

## Secure Execution Process (안전한 실행 프로세스)

When running an encrypted Python file, Sloth-Lock follows these secure steps:

암호화된 Python 파일을 실행할 때, Sloth-Lock은 다음과 같은 안전한 단계를 거칩니다:

1. **Memory-based Decryption (메모리 기반 복호화)**
   - The encrypted file is decrypted in memory only
   - No temporary files are written to disk
   - Original encrypted file remains unchanged
   
   - 암호화된 파일은 메모리에서만 복호화됩니다
   - 디스크에 임시 파일이 생성되지 않습니다
   - 원본 암호화 파일은 그대로 유지됩니다

2. **Secure Module Loading (안전한 모듈 로딩)**
   - Decrypted code is loaded as a Python module
   - Code execution happens in a controlled environment
   - Memory is cleared after execution
   
   - 복호화된 코드는 Python 모듈로 로드됩니다
   - 코드 실행은 제어된 환경에서 이루어집니다
   - 실행 후 메모리는 자동으로 정리됩니다

3. **Password Protection (비밀번호 보호)**
   - Password is required for each execution
   - Password is never stored or cached
   - Each run requires fresh authentication
   
   - 매 실행마다 비밀번호가 필요합니다
   - 비밀번호는 저장되거나 캐시되지 않습니다
   - 각 실행마다 새로운 인증이 필요합니다

## Error Messages (오류 메시지)

The tool provides clear error messages in both English and Korean:

이 도구는 영어와 한국어로 명확한 오류 메시지를 제공합니다:

### Wrong Password (잘못된 비밀번호)
```
[Error] Decryption failed
Cause: Invalid password entered
Solution: Please enter the exact password used for encryption

[오류] 복호화에 실패했습니다
원인: 잘못된 비밀번호를 입력하셨습니다
해결 방법: 암호화할 때 사용한 비밀번호를 정확히 입력해주세요
```

### File Not Found (파일을 찾을 수 없음)
```
[Error] File not found
Cause: The specified file does not exist
Solution: Please check if the file path is correct

[오류] 파일을 찾을 수 없습니다
원인: 지정된 파일이 존재하지 않습니다
해결 방법: 파일 경로가 올바른지 확인해주세요
```

## Security Notes (보안 참고사항)

- Always use strong passwords
- Keep your passwords secure
- Encrypted files cannot be recovered without the correct password

- 강력한 비밀번호를 사용하세요
- 비밀번호를 안전하게 보관하세요
- 암호화된 파일은 올바른 비밀번호 없이 복구할 수 없습니다

## License (라이선스)

MIT License

## Author (작성자)

cryingmiso 