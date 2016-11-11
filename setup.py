from setuptools import setup, find_packages


setup(
    name='lagmonitor',
    version='1.0.0',
    description='Report Kafka lag statistics to statsd',
    author='Luc Russell',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.4'
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'spec*']),
    install_requires=[
        'docopt',
        'pyyaml',
        'pykafka'
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'lagmonitor = lagmonitor.main:main'
        ],
    },
)
