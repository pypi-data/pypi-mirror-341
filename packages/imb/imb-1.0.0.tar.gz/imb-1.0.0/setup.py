from setuptools import setup, find_packages
import os


def req_file(filename="requirements.txt", folder=""):
    with open(os.path.join(folder, filename)) as f:
        content = f.readlines()
    return [x.strip() for x in content if not x.startswith("#")]

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='imb',
    version='1.0.0',
    author='p-constant',
    author_email='nikshorop@gmail.com',
    description='Python library for run inference of deep learning models in different backends',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/TheConstant3/InferenceMultiBackend',
    packages=find_packages(),
    install_requires=req_file(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)
