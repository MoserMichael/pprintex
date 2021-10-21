import os
import setuptools 

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setuptools.setup(
    name = "printex", 
    version = "0.0.7",
    author = "Michael Moser",
    author_email = "moser.michael@gmail.com",
    description = ("similar to pprint, but shows all object field values."),
    license = "MIT",                                                               
    keywords = "debugging, tracing, pretty printing",
    url = "https://github.com/MoserMichael/pprintex",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Logging",
        "Topic :: Utilities"
    ],
    python_requires='>=3.3',
)
