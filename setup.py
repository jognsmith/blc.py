from setuptools import setup

if __name__ != "__main__":
    import sys
    sys.exit(1)

def long_desc(ext="md"):
    # Markdown because I CBF to do reST.
    with open('README.{0}'.format(ext), 'rb') as f:
        return f.read()

kw = {
    "name": "blc.py",
    "version": "1.0.0",
    "description": "An easy way to interact with the BlooCoin environment.",
    "long_description": long_desc(),
    "url": "https://github.com/jognsmith/blc.py",
    "author": "John Smith",
    "author_email": "jogn.smith@riseup.net",
    "license": "MIT",
    "packages": ["blcpy"],
    "zip_safe": False,
    "keywords": "bloocoin wrapper client",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
}

if __name__ == "__main__":
    setup(**kw)
