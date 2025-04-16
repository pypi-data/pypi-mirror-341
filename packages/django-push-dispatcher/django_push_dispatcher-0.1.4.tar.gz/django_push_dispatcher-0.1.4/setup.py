from setuptools import setup, find_packages

setup(
    name="django-push-dispatcher",  # Name of your package
    version="0.1.4",                # Initial version
    packages=find_packages(),       # Automatically find all packages
    include_package_data=True,      # Include additional files like templates, static, etc.
    install_requires=[              # List of dependencies
        'django>=3.0,<5.2',         # Django version compatibility
        'firebase-admin>=5.0.0',    # Firebase Admin SDK
        'requests>=2.0.0',          # For sending HTTP requests
    ],
    extras_require={                # Optional dependencies
        'dev': ['pytest', 'tox'],   # For development/testing
    },
    long_description=open('README.md').read(),  # To load your README as the long description
    long_description_content_type='text/markdown',  # Format for the README
    classifiers=[                  # Classifiers for PyPi
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',         # Compatible with Python >= 3.6
)
