from setuptools import setup, find_packages

setup(
    name='sbanetwork',
    version='0.1.1',
    description='Lightweight Neural Network Library from scratch',
    author='Abhishek Gupta',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description_content_type='text/markdown',
)
