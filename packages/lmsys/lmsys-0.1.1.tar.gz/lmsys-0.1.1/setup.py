from setuptools import setup

setup(
    name="lmsys",
    version="0.0.1",
    description="A python sdk for coding through scripting",
    author="Sean Sullivan",
    author_email="sean@lmsystems.ai",
    py_modules=["aider_sdk"],
    install_requires=[
        "aider-chat>=0.82.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)