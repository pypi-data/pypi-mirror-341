from setuptools import setup, find_packages

setup(
    name='butterrand',
    version='0.1.2',
    description='Random number generator based on butterfly effect and chaotic maps',
    author='Bùi Phong Phú',
    author_email='omerasutvail@gmail.com',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.7',
    license='MIT',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
