from setuptools import setup, find_packages

setup(
    name='salahhemdan',
    version='0.1',
    description='social downloader Vedio & Images',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Salah Hemdan',
    author_email='your@email.com',
    url='https://github.com/yourusername/salahhemdan',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
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
