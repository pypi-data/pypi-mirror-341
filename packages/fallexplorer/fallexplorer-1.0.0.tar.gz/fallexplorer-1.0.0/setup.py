from setuptools import setup, find_packages

setup(
    name='fallexplorer',
    version='1.0.0',
    description='Outil de pentesting avec reconnaissance passive et tests actifs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ton Nom',
    author_email='contact@openstudy.me',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-whois',
        'dnspython',
        'builtwith',
        'tabulate',
        'rich'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)