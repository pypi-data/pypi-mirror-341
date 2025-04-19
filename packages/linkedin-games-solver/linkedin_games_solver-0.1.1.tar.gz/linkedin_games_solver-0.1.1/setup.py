from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="linkedin-games-solver",
    version="0.1.1",
    author="Zane Bookbinder",
    url="https://github.com/zanebookbinder/LinkedIn-Games-Solver",
    description="A solver for LinkedIn's puzzle games using Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "attrs==25.3.0",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "h11==0.14.0",
        "idna==3.10",
        "outcome==1.3.0.post0",
        "PySocks==1.7.1",
        "readchar==4.2.1",
        "rich==14.0.0",
        "selenium==4.31.0",
        "sniffio==1.3.1",
        "sortedcontainers==2.4.0",
        "trio==0.29.0",
        "trio-websocket==0.12.2",
        "typing_extensions==4.13.1",
        "urllib3==2.3.0",
        "websocket-client==1.8.0",
        "websockets==15.0.1",
        "wsproto==1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedin-solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin_games_solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin-games-solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin_solver=linkedin_games_solver.solver:main",  # CLI command
            "solver=linkedin_games_solver.solver:main",  # CLI command
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
