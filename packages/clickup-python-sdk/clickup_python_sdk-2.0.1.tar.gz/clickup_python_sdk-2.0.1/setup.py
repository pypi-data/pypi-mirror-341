from setuptools import setup, find_packages
import os

# Read long description from README.md if it exists, otherwise use README.txt
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    long_description_content_type = "text/markdown"
else:
    with open("README.txt", "r", encoding="utf-8") as f:
        long_description = f.read()
    long_description_content_type = "text/plain"

setup(
    name="clickup-python-sdk",
    version="2.0.1",  # Match VERSION in config.py
    description="Python SDK for the ClickUp API",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author="Michael Broyles",
    author_email="michaelbroyles68@gmail.com",
    url="https://github.com/MB0390231/clickup_python_sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "certifi>=2025.1.31",
        "charset-normalizer>=3.4.1",
        "idna>=3.10",
        "urllib3>=2.4.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="clickup, api, sdk, productivity, task management",
    python_requires=">=3.7",
    project_urls={
        "Bug Tracker": "https://github.com/MB0390231/clickup_python_sdk/issues",
        "Documentation": "https://github.com/MB0390231/clickup_python_sdk",
        "Source Code": "https://github.com/MB0390231/clickup_python_sdk",
    },
)
