from setuptools import setup, find_packages

setup(
    name="huawuque-cryptool",
    version="0.1.8",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cryptool': ['utils/*.py'],
    },
    install_requires=[
        'cryptography>=3.4.7',
        'mysql-connector-python>=8.0.26',
        'python-dotenv>=0.19.0',
        'tkinter',
    ],
    entry_points={
        'console_scripts': [
            'cryptool=cryptool.cli.main:main',
            'cryptool-gui=cryptool.gui.main:main',
        ],
    },
    author="HuaWuQue",
    author_email="huawuque@example.com",
    description="A comprehensive encryption tool with GUI and CLI interfaces",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/huawuque/EncryptionTool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 