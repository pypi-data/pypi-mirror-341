from setuptools import setup, find_packages

setup(
    name='linkanalys',                     # Your package name
    version='0.1.0',                    # Version
    description='''Link Analysis and PageRank
    ● Implement the PageRank algorithm to rank web pages based on link analysis.
    ● Apply the PageRank algorithm to a small web graph and analyze the results. ''',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
