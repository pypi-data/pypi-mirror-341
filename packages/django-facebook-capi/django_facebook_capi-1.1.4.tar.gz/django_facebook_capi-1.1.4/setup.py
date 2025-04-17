# setup.py
from setuptools import setup, find_packages

setup(
    name='django_facebook_capi',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Reusable Django app to track Meta/Facebook CAPI events server-side.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Weird-Labs-Pvt-Ltd/djang-facebook-capi',  # your repo
    author='Preet Sonpal',
    author_email='preet@weirdlabs.in',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
    install_requires=[
        'Django>=3.2',
        'requests',
    ],
    python_requires='>=3.7',
)
