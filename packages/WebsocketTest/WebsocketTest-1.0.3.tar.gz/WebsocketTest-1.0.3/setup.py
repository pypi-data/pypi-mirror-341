from setuptools import find_packages, setup


setup(
    name="WebsocketTest",
    version="1.0.3",
    author='chencheng',
    python_requires=">=3.10",
    packages=find_packages(exclude=["WebsocketTest.allure_report", "WebsocketTest.logs", "WebsocketTest.allure_results",  "WebsocketTest.config", "WebsocketTest.data"]),
    description="websocket api autotest",
    # long_description=open('README.md','r',encoding='utf-8').read(),
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
            'wsrun=WebsocketTest.cli:main_run_alias'
        ]
    }
)