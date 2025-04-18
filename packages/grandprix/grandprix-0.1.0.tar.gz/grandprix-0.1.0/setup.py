from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='grandprix',
    version='0.1.0',
    author='Idin K',
    author_email='python@idin.net',
    description='A Python package for Formula 1 data analysis and visualization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/idin/grandprix',
    packages=find_packages(),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
) 