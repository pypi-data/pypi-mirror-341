from setuptools import setup, find_packages

setup(
    name="sudoh",
    version="0.1.0",
    description="A simple CLI tool that automatically re-runs your last shell command with sudo. If you get a permissions error, just type sudoh to repeat your previous command as root. Supports bash and zsh.",
    author="Your Name",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sudoh=sudoh.cli:main'
        ],
    },
    python_requires='>=3.6',
)
