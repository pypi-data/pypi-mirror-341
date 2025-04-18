from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("LICENSE", "r") as f:
    license_text = f.read()

setup(
    name="pyimgcaptcha",
    version="0.1.0",               
    author="redderi",
    author_email="vrudko22@gmail.com",
    description="Library for generating CAPTCHA images",
    long_description=long_description + "\n\n" + license_text,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[             
        "Pillow>=8.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT", 
    license_files=("LICENSE",),     
)