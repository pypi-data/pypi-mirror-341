from setuptools import setup

setup(
    name="mcp_server_time_test",
    version="0.1",
    packages=["mcp_server_time"],
    install_requires=["fastapi", "uvicorn"],
    entry_points={
        "console_scripts": [
            "mcp-time=mcp_server_time.__main__:main"
        ]
    }
)
