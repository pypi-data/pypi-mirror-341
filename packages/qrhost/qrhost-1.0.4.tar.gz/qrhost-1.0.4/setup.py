from setuptools import setup, find_packages

setup(
    name='qrhost',
    version='1.0.4',
    description='A tool for hosting files and directories with QR codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hamdaoui Ryan',
    author_email='ryanhamdaoui45@gmail.com',
    url='https://github.com/ryanhamdaoui/qrhost',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'qrcode',
        'netifaces',
    ],
    license='MIT',  # Explicit license field
    entry_points={
        'console_scripts': [
            'qrhost = qrhost.qrhost:main',  # Points to the main function inside qrhost.py
        ],
    },
    python_requires='>=3.6',
)
