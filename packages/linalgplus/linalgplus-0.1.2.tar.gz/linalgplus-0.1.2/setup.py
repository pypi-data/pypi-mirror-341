from setuptools import setup, find_packages

setup(
    name='linalgplus',  # lowercase, no spaces
    version='0.1.2',
    author='Your Name',
    author_email='you@example.com',
    description='A lightweight linear algebra library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/linalgplus',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
