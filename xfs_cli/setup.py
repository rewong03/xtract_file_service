from setuptools import setup

setup(
    name='xfs',
    version='0.1',
    py_modules=['xtract_file_service_cli'],
    install_requires=[
        'Click', 'pyunpack', 'patool', 'requests'
    ],
    entry_points='''
        [console_scripts]
        xfs=xtract_file_service_cli:xfs_cli
    ''',
)