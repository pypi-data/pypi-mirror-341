from setuptools import setup, find_packages

setup(
    name='clusterir',                     # Your package name
    version='0.1.0',                    # Version
    description='''Clustering for Information Retrieval
    ● Implement a clustering algorithm (e.g., K-means or hierarchical clustering).
    ● Apply the clustering algorithm to a set of documents and evaluate the clustering results.''',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
