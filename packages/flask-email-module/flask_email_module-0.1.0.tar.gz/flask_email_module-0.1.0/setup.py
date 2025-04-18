from setuptools import setup, find_packages

setup(
    name='flask_email_module',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    python_requires='>=3.6',
    author='Baskar',
    author_email='newtonbaskar04@gmail.com',
    description='A Flask module that captures login form data and sends it via email.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Baskar245/flask_email_module',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: OS Independent',
    ],
)
