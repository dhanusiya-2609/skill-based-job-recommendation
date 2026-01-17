"""
Setup script for the Skill-Based Job Recommendation System
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='skill-job-recommendation-system',
    version='1.0.0',
    description='AI-powered job recommendation system based on user skills',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/skill-job-recommendation-system',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.4.4',
            'black>=24.1.1',
            'flake8>=7.0.0',
            'mypy>=1.8.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'job-rec=run:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)