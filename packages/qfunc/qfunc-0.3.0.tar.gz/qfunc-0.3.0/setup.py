from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qfunc",
    version="0.3.0",
    author="Mozahidul Islam",
    author_email="mirivan722@gmail.com",
    description="Interactive error handling and debugging for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mi-rivan/qf.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
    ],
    python_requires=">=3.6",
)