from setuptools import setup, find_packages

setup(
    name='evaluationmetric',                     # Your package name
    version='0.1.1',                    # Version
    description='Evaluation Metrics for IR Systems',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
