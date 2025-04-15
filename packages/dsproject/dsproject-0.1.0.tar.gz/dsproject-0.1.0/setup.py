from setuptools import setup, find_packages

setup(
    name='dsproject',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'dsproject=dsproject.cli:main',  # Optional: If you want a CLI entry point
        ],
    },
    author='ATS',
    author_email='arumugatamilselvan@example.com',
    description='A Data Science project for model training and data exploration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/dsproject',  # GitHub link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
