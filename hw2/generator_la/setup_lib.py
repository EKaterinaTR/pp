from setuptools import setup, find_packages

setup(
    name="latex_generator_ts",
    version="0.4.0",
    author="Katya Ts",
    author_email="ekaterinatsr@gmail.com",
    description="A library for generating LaTeX tables and images.",
    packages=['hw2/generator_la/generator_latex'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)