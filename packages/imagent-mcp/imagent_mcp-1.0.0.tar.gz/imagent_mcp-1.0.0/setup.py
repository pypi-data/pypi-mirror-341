from setuptools import setup, find_packages

setup(
    name="imagent-mcp",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp[cli]>=1.6.0",
        "pillow>=11.2.1",
    ],
    python_requires=">=3.13",
    author="Dave Lee",
    author_email="dream@fun-coding.org",
    description="AI-powered local image management and organization tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/imagent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
    ],
) 