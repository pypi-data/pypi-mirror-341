from setuptools import setup, find_packages

setup(
    name="securepassgen-advanced",  # New name
    version="1.0.0",
    description="Advanced password generator library",
    author="cipherh4ck",
    author_email="emerickcipher@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'securepassgen-cli=securepassgen.cli:main',
        ]
    },
    install_requires=[],  # Add dependencies here if needed (like pyperclip)
    python_requires='>=3.6',
)
