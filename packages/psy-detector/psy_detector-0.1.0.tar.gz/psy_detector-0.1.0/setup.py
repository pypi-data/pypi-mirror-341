from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="psy-detector",
    version="0.1.0",
    author="SemiQuant",
    author_email="your.email@example.com",
    description="A real-time sigh detection system using audio processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/psy-detector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "librosa>=0.10.1",
        "numpy>=1.24.0",
        "click>=8.1.7",
        "soundfile>=0.12.1",
        "scipy>=1.10.0",
        "rich>=13.7.0",
        "matplotlib>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "psy-detector=sigh_detector:main",
        ],
    },
) 