from setuptools import setup, find_packages

setup(
    name="lin-autopilot-tools",
    version="0.1.0",
    author="Your Name",
    author_email="august0703@163.com",
    description="A short description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",  # 依赖项
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)