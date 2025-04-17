from setuptools import setup, find_packages

setup(
    name='mora',
    version='0.2.0',
    author='omar',
    author_email='',
    description='Self-contained Python remote administration library',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)