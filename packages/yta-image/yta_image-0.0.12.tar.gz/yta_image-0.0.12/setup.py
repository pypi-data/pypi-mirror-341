from setuptools import setup, find_packages


VERSION = '0.0.12'
DESCRIPTION = 'Youtube Image Module.'
LONG_DESCRIPTION = 'This is the Youtube Autonomous Image module'

setup(
    name = "yta_image", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_general_utils',
        'yta_ai_utils',
        'pillow',
        'pillow-lut',
        # This 'backgroundremover' could be removed if we don't need its functionality (only 1)
        'backgroundremover',
        'numpy',
        'scikit-image',
        'opencv-python',
        # This 'imutils' library has been commented because I don't see code using it
        #'imutils'
    ],
    
    keywords = [
        'youtube autonomous image module software'
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