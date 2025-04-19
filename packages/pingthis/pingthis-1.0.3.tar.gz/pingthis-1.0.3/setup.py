from setuptools import setup, find_packages

setup(
    name='pingthis',
    version='1.0.3',
    packages=find_packages(),  # Automatically find packages
    entry_points={
        'console_scripts': [
            'pingthis = pingthis.__main__:main'
        ],
    },
    install_requires=[
        'rich',
    ],
    author='eytin',
    description='A simple internal network pinging tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eytin/pingthis',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
