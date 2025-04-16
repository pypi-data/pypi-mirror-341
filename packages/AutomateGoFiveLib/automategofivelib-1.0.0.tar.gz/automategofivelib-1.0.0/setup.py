from setuptools import setup, find_packages

setup(
    name="AutomateGoFiveLib",
    version="1.0.0",
    author="Pornpawit Suttha",
    author_email="pornpawit14suttha@gmail.com",
    description="Test Library for AutomateGoFiveLib",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pornpawitsuttha/AutomateGoFiveLib.git",
    packages=find_packages(),
    install_requires=[
        'robotframework>=3.0',
        'pytz',
        'numpy',
        'pillow',
        'opencv-python',
        'matplotlib',
        'pymongo'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)