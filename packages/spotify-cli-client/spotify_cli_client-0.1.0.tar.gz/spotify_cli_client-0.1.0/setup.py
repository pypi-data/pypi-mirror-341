from setuptools import find_packages, setup

setup(
    name="spotify-cli-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click", "spotipy", "InquirerPy"],
    entry_points={
        "console_scripts": [
            "spt = spotify_cli_client.cli:cli",
        ],
    },
    author="Sudharshan V",
    author_email="sudarshan61kv@gmail.com",
    description="Simple Spotify Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
