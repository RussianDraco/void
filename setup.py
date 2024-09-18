from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

setup(
    name="void",
    version="0.1.2",
    author="Ivan Sivakov",
    license="MIT",
    description="A manager for Python-based games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RussianDraco/void",
    py_modules=["void", "app"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    entry_points='''
        [console_scripts]
        void=void:cli
    '''
)