
from setuptools import setup, find_packages

setup(
    name="mseep-mcp2mqtt",
    version="0.1.0",
    description="MCP MQTT Service for PWM Control and Device Communication",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['pyyaml>=6.0.1', 'paho-mqtt>=1.6.1', 'mcp-python>=0.1.0'],
    keywords=["mseep"] + ['mcp', 'mqtt', 'pwm', 'control', 'device', 'communication'],
)
