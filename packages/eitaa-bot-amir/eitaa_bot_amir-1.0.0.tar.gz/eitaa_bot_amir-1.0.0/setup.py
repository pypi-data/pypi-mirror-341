from setuptools import setup, find_packages  

setup(  
    name='eitaa_bot_amir',  
    version='1.0.0',  
    description='A Python package for interacting with Eitaa Bot API',  
    long_description='A Python package that provides a convenient way to interact with Eitaa Bot API.\n\n'  
                     '## Features\n'  
                     '- Send messages\n'  
                     '- Send photos\n'  
                     '- Send files and documents\n'  
                     '...\n\n'  
                     '## Install\n'  
                     '```bash\n'  
                     'pip install eitaa_bot\n'  
                     '```\n\n'  
                     '## Usage\n'  
                     '```python\n'  
                     'from eitaa_bot import EitaaBot\n'  
                     '...\n'  
                     '```',  
    long_description_content_type='text/markdown',  
    author='AmirhossiKhazai',  
    author_email='amirhossinpython03@gmail.com',  
    url='https://github.com/amirhossinpython/eitaabot',  
    packages=find_packages(),  
    install_requires=[  
        'requests',  
    ],  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
)  