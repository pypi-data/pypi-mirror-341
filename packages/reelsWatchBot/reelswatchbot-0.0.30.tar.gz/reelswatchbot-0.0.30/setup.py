from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.30'
DESCRIPTION = 'A Python package to create a telegram bot that can download Instagram Reels from any public Instagram page.'
LONG_DESCRIPTION = 'reelsWatchBot is a Python package that allows you to create a Telegram bot that can download Instagram Reels from any public Instagram page. The bot uses the Instapy package to download the reels from the links sent by the users. The bot can be customized to handle different types of messages and commands, and can be deployed on any platform that supports Python. The package is easy to use and can be customized to suit your needs.'

setup(
    name="reelsWatchBot",
    version=VERSION,
    author="djalti",
    author_email="abdeldjalilselamnia@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['insta-scrape-py', 'python-telegram-bot'],
    keywords=['python', 'instagram', 'scrape', 'download', 'reels', 'pages', 'telegram', 'bot', 'automation'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)