from setuptools import setup, find_packages

setup(
    name="huawuque-cryptool",
    version="0.1.6",
    packages=find_packages(),
    package_data={
        'cryptool': ['core/*.py', 'cli/*.py', 'gui/*.py', 'utils/*.py'],
    },
    install_requires=[
        "python-dotenv>=1.0.0",
        "cryptography>=41.0.0",
        "python-docx==0.8.11",
        "docx2txt==0.8",
        "pycryptodome>=3.18.0",
        "mysql-connector-python>=8.0.0",
        "psutil>=5.9.0",
    ],
    author="huawuque",
    author_email="huawuque555@gmail.com",
    description="A comprehensive encryption tool supporting multiple algorithms",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/huawuque/cryptool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cryptool=cryptool.cli.main:main",
            "cryptool-gui=cryptool.gui.main_window:main",
        ],
    },
) 