from setuptools import setup, find_packages

setup(
    name="nawa-tracking",
    version="0.1.0",
    description="NAWA – Smart Pilgrim Tracking & AI Toolkit",
    author="Khalid Al-...",
    license="Apache License 2.0",
    packages=find_packages(),
    install_requires=[
        "fpdf2==2.7.7",
        "boto3>=1.34"
    ],
    python_requires=">=3.8",
    url="https://github.com/kapp1/nawa-smart-hajj",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

