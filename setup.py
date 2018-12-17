from setuptools import setup, find_packages

setup(
    name='django-inlineobjects',
    packages=find_packages(),
    version='1.1.0',
    description='A reusable Django application used to insert content objects into other pieces of content.',
    author='Peter Hogg',
    author_email='peter@havenaut.net',
    url='https://github.com/pigmonkey/django-inlineobjects',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
    ],
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['BeautifulSoup4>=4.4.0'],
)
