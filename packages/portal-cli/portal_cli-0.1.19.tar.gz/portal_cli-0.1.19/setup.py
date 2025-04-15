from setuptools import setup

setup(
    name='portal-cli',
    version='0.1.19', 
    packages=['commands'], 
    py_modules=['main_cli'],
    entry_points={
        'console_scripts': [
            'portal-cli = main_cli:cli',
        ],
    },
    install_requires=[
        'click',
        'requests',
    ],
    author='AI Cloud Services LLC',
    author_email='barb.rock@k8or.com',
    description='A CLI for portal image management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/k8or-orbit-aws/portal-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['main_cli.py'],
    },
)

