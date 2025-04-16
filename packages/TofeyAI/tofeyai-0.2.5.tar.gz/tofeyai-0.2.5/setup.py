from setuptools import setup, find_packages

setup(
    name='TofeyAI',
    version='0.2.5',
    description='مكتبة ذكاء اصطناعي توفي AI',
    author='Tofey',
    author_email='techuruk@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
