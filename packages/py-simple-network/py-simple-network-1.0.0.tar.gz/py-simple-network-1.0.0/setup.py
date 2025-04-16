from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='py-simple-network',
    version='1.0.0',
    description='A Python library for simple TCP-based client-server communication',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GeovaneDev54',
    author_email='geovanethecoder@gmail.com',
    url='https://github.com/GeovaneDev54/py-simple-network',
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)