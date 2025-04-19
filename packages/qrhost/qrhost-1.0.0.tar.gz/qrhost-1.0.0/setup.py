from setuptools import setup, find_packages

setup(
    name='qrhost',
    version='1.0.0',  
    description='A tool for hosting files and directories with QR codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hamdaoui Ryan',
    author_email='ryanhamdaoui45@gmail.com',
    url='https://github.com/ryanhamdaoui/qrhost',  
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Correct classifier
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'qrcode',
        'netifaces',
    ],
    license='MIT',  # Add explicit license field
    entry_points={
        'console_scripts': [
            'qrhost = qrhost.file_host_qr:main',  # Ensure this points to the correct script and function
        ],
    },
    python_requires='>=3.6', 
)
