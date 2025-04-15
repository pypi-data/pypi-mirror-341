from setuptools import setup, find_packages

setup(
    name="sloth-lock",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "cryptography>=42.0.0",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "slock-enc=src.cli:encrypt",
            "slock-dec=src.cli:decrypt",
            "slock-run=src.run_encrypted:main",
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