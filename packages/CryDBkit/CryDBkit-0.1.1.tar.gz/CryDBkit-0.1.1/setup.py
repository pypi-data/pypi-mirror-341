import os
from setuptools import setup, find_packages

setup(
    name='CryDBkit',
    version='0.1.1',
    description="ToolKit for building your own Crystal Database",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='CaoBin',
    author_email='binjacobcao@gmail.com',
    maintainer='CaoBin',
    maintainer_email='binjacobcao@gmail.com',
    license='MIT License',
    url='https://github.com/WPEM',
    packages=find_packages(include=['CryDBkit', 'CryDBkit.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.5',
    install_requires=[
        'wget'
    ],

)
