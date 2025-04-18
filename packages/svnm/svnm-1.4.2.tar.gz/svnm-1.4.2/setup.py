from setuptools import setup, find_packages

setup(
    name="svnm",
    version="1.4.2",
    author="svn.murali",
    author_email="svnmurali1@gmail.com",
    description="A package to make the usage of DeepLearning models easier",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/svnmurali-2004/svnm",  # Replace with your GitHub URL
    
    install_requires=[
       "huggingface_hub",
"matplotlib",
"numpy",
"pandas",
"pyfiglet",
"setuptools",
"tensorflow-cpu",
"termcolor",
"ultralytics",
"opencv-python",
"keras_facenet",
"deepface"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
