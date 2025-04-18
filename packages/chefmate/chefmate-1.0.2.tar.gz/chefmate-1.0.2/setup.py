from setuptools import setup, find_packages

setup(
    name='chefmate', 
    version='1.0.2', 
    author='Anuj Kumar Sah',
    author_email='anujsah282005@gmail.com',
    description='A CodeChef automation CLI tool',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anuj-72/ChefMate',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'webdriver-manager',
        'click',
        'colorama',
        'inquirer',
        'InquirerPy',
        'rich',
        'tabulate',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'chefmate=chefmate.cli:interactive',  
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
