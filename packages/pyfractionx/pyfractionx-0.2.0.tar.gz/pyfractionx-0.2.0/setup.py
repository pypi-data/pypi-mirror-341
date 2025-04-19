from setuptools import setup, find_packages

setup(
    name='pyfractionx',
    version='0.2.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A custom fraction math library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/spremrahul007/pyfractionx',
    packages=find_packages(),  # now it will find pyfractionx
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
