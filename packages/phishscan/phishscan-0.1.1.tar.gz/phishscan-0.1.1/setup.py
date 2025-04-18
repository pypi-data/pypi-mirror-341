from setuptools import setup, find_packages

setup(
    name="phishscan",  # Name of your package
    version="0.1.1",     # Version number
    packages=find_packages(),  # Automatically find your package(s)
    install_requires=[        # Dependencies that need to be installed via pip
        'beautifulsoup4',
        'confusables',
    ],
    entry_points={  # This allows you to call your script from the command line
        'console_scripts': [
            'phishscan = phishscan.cli:main',  # phishscan will run main.py
        ],
    },
    long_description=open('README.md').read(),  # Optional: Readme file for description
    long_description_content_type='text/markdown',  # Optional: Readme format
    author="Makara_Chann",  # Replace with your name
    author_email="makara.chann.work@gmail.com",  # Replace with your email
    description="Phishing Email Scanner",  # Short description of the package
    license="MIT",  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update if using a different license
        'Operating System :: OS Independent',
    ],
)
