from setuptools import setup, find_packages

setup(
    name="instapytool",
    version="0.1.1",
    author="Prajjwal Nag",
    author_email="your.email@example.com",  # Replace with your email
    description="Send Instagram DMs using session ID automation with Selenium",
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prajjwalnag/InstaPy",
    project_urls={
        "Source": "https://github.com/prajjwalnag/InstaPy",
        "Bug Tracker": "https://github.com/prajjwalnag/InstaPy/issues",
    },
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        "fastapi>=0.78.0",
        "pydantic>=1.10.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',
)
