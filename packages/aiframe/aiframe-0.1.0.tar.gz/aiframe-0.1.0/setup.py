from setuptools import find_packages, setup

setup(
    name="aiframe",
    version="0.1.0",
    author="Enrique Leal",
    author_email="",
    packages=find_packages(),
    install_requires=["aiohttp", "nest_asyncio", "pandas", "python-dotenv", "tqdm"],
    python_requires=">=3.6",
    description="Open-source library for lightweight, fast batch enhancement of Python pandas DataFrames using Gen-AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lealcastillo1996/AIFrame",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
