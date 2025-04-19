from setuptools import setup, find_packages

setup(
    name="linkedin-games-solver",
    version="0.1.0",
    author="Zane Bookbinder",
	url="https://github.com/zanebookbinder/LinkedIn-Games-Solver",
    description="A solver for LinkedIn's puzzle games using Selenium",
    packages=find_packages(),
    install_requires=[
        "attrs==25.3.0",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "h11==0.14.0",
        "idna==3.10",
        "outcome==1.3.0.post0",
        "PySocks==1.7.1",
        "selenium==4.31.0",
        "sniffio==1.3.1",
        "sortedcontainers==2.4.0",
        "trio==0.29.0",
        "trio-websocket==0.12.2",
        "typing_extensions==4.13.1",
        "urllib3==2.3.0",
        "websocket-client==1.8.0",
        "websockets==15.0.1",
        "wsproto==1.2.0"
    ],
    entry_points={
        "console_scripts": [
            "linkedin-solver=linkedin_games_solver.solver:main",  # CLI command
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
