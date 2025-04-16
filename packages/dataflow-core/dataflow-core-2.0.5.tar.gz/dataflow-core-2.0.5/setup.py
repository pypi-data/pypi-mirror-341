from setuptools import setup, find_packages

setup(
    name="dataflow-core",
    version="2.0.5",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={},
    install_requires=[
        'sqlalchemy',
        'boto3',
        'psycopg2-binary',
        'pymysql',
        'requests'
    ],
    author="Dataflow",
    author_email="",
    description="Dataflow core package",
    entry_points={
        'jupyterhub.authenticators': [
            'dataflow_authenticator = authenticator.dataflowhubauthenticator:DataflowHubAuthenticator',
        ],
    },
)