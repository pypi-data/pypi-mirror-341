import setuptools
VERSION = '1.0.23'
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()
setuptools.setup(
    name='Httppool',
    version=VERSION,
    author='alexdev',
    author_email='alexdev.workenv@gmail.com',
    description='Get and storing the HTML data of a website using a cache system.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/alexdevzz/httppool-ce-services.git',
    project_urls={
        'Bug Tracker': 'https://github.com/alexdevzz/httppool-ce-services/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[
        'requests',
    ],
)
