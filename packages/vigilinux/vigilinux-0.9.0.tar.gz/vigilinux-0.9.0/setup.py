from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vigilinux",  # Changed the name to vigilinux
    version="0.9.0",
    author="Subhan_Rauf",
    author_email="raufsubhan45@gmail.com",
    description="Vigi is an AI assistant for running commands in natural language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naumanAhmed3/VigiLinux-Shell-Interpreter",
    packages=find_packages(),
    package_data={"vigilinux": ["settings.json"]},  # Changed to vigilinux
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "google-generativeai",
        "python-dotenv==0.19.2",
        "setuptools",
        "importlib_resources",
    ],
    entry_points={
        "console_scripts": [
            "vigi=vigilinux.main:main",  # Keeping the terminal command as "vigi"
        ],
    },
)
