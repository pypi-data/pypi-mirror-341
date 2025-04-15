from setuptools import setup, find_packages

setup(
    name='municipality-lookup',
    version='0.2.0',
    author='Andrea Iannazzo',
    author_email='andrea.iannazzo@gmail.com',
    description='Fuzzy and exact lookup tool for Italian municipalities',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/andrjan1/municipality-lookup',
    packages=find_packages(),
    package_data={'municipality_lookup': ['data/comuni.csv']},
    include_package_data=True,
    install_requires=['pandas','rapidfuzz'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
)
