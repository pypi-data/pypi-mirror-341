from setuptools import setup, find_packages


setup(
    name='resistant_kafka',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        "confluent-kafka==2.8.2",
        "dotenv==0.9.9",
        "requests==2.32.3",
        "pydantic==1.10.21"
    ]
)
