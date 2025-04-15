from setuptools import setup, find_packages

setup(
    name='MM18021UNO',
    version='0.1.1',
    packages=find_packages(),
    description='Librería de métodos numéricos para resolver ecuaciones lineales y no lineales',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Claudia',
    author_email='mm18021@ues.edu.sv',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'sympy',
    ],
)
