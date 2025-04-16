import setuptools

with open('readme.md') as fp:
    long_description = fp.read()

with open('requirements.txt') as fp:
    requirements = fp.read().splitlines()

setuptools.setup(
    name='preprocess_nlp_jp18',
    include_package_data=True,
    version='0.3',
    author='Jayesh Padiya',
    description='This is a text preprocessing package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)
