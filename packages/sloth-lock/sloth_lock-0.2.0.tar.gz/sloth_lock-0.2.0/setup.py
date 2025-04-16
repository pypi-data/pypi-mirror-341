from setuptools import setup, find_packages

setup(
    name="sloth-lock",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "cryptography>=42.0.0",
        "click>=8.1.7",
        "astroid>=2.15.0",  # 의존성 분석을 위해
    ],
    entry_points={
        "console_scripts": [
            "slock-enc=slock.cli.cli:encrypt",
            "slock-dec=slock.cli.cli:decrypt",
            "slock-enc-dir=slock.cli.cli:encrypt_dir",
            "slock-run-dir=slock.cli.cli:run_dir",
        ],
    },
    author="cryingmiso",
    author_email="if.sloth@gmail.com",
    description="파일 암호화/복호화 도구 (File Encryption/Decryption Tool)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cryingmiso/slock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Korean",
        "Natural Language :: English",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.6",
) 