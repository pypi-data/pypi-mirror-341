from setuptools import setup, find_packages

setup(
    name='pingthis',
    version='1.0.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pingthis = pingthis.__main__:main',
        ],
    },
    install_requires=[
        'rich',
    ],
    author='eytin',
    description='Terminal ping tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
