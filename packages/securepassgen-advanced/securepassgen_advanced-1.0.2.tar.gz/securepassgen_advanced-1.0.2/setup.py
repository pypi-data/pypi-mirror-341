from setuptools import setup, find_packages

setup(
    name="securepassgen-advanced",  # New name
    version="1.0.2",  # Bump the version for the fix
    description="Advanced password generator library",
    author="cipherh4ck",
    author_email="emerickcipher@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'securepassgen-cli=securepassgen_advanced.cli:main',  # Fixed module path
        ]
    },
    install_requires=[],
    python_requires='>=3.6',
)
