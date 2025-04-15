from setuptools import setup, find_packages

setup(
    name='OS23002UNO',
    version='1.0.1',
    packages=find_packages(),
    description='Librería en Python para resolver sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexis Orantes',
    author_email='os23002@gmail.com',
    url='https://github.com/usuario/ecusolver',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
    ],
    python_requires='>=3.6',
    install_requires=['numpy'],
)
