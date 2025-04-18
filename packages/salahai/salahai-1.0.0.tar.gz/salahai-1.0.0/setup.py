from setuptools import setup, find_packages

setup(
    name='salahai',
    version='1.0.0',
    description='SalahAi - ذكاء اصطناعي ذكي',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Salah Hemdan',
    author_email='salah1hemdaan@gmail.com',
    url='https://facebook.com/cap.salah.hemdan',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)