from setuptools import find_packages, setup


setup(
    name="WebsocketTest",
    version="1.0.0",
    author='chencheng',
    python_requires=">=3.7",
    packages=find_packages(exclude=["examples", "logs", "tests.*"]),
    description="websocket api autotest",
    long_description=open('README.md','r',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires = [
        "allure_python_commons==2.13.5",
        "numpy==2.2.4",
        "pandas==2.2.3",
        "pytest==8.2.2",
        "PyYAML==6.0.2",
        "websockets==12.0"
    ],
    entry_points={
        'console_scripts': [
            'har2case=pastor.cli:main_har2case_alias',
            'pmake=pastor.cli:main_make_alias',
            'prun=pastor.cli:main_prun_alias',
            'pastor=pastor.cli:main',
            'locusts=pastor.ext.locust:main_locusts'
        ]
    }
)