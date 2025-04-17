from setuptools import setup, find_packages

setup(
    name='textcat',                     # Your package name
    version='0.1.0',                    # Version
    description='''Text Categorization
    ● Implement a text classification algorithm (e.g., Naive Bayes or Support Vector Machines).
    ● Train the classifier on a labelled dataset and evaluate its performance.''',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
