from setuptools import setup, find_packages

setup(
    name="lsdk",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "lsdk = lsdk.cli:main"
        ]
    },
    install_requires=[
        "pyinstaller"
    ],
    author="panoscodergr",
    description="Lightweight SDK builder for Python apps",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
