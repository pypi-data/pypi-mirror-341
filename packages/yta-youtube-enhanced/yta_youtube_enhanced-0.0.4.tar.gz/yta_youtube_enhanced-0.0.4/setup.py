from setuptools import setup, find_packages


VERSION = '0.0.4'
DESCRIPTION = 'Youtube Autonomous Youtube enhanced module.'
LONG_DESCRIPTION = 'Youtube Autonomous Youtube interaction module package is built to enhance the basic interaction with Youtube platform by applying AI.'

setup(
    name = "yta_youtube_enhanced", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_youtube',
        'yta_general_utils',
        'yta_ai_utils'
    ],
    
    keywords = [
        'youtube autonomous youtube enhanced module',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)