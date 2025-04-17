from setuptools import setup, find_packages

setup(
    name="django-push-dispatcher",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.0,<5.2',
        'firebase-admin>=5.0.0',
        'requests>=2.0.0',
    ],
    extras_require={
        'dev': ['pytest', 'tox'],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
