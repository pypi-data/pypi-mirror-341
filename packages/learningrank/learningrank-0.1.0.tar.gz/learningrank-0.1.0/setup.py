from setuptools import setup, find_packages

setup(
    name='learningrank',                     # Your package name
    version='0.1.0',                    # Version
    description='''Learning to Rank
    ● Implement a learning to rank algorithm (e.g., RankSVM or RankBoost).
    ● Train the ranking model using labelled data and evaluate its effectiveness. ''',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
