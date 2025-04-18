from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define the Cython extension
extensions = [
    Extension(
        name="cosine_utils",
        sources=["cosine_utils/cosine_utils.pyx"],
        include_dirs=[np.get_include()],  # Include NumPy headers
    )
]

# Setup function to build the package
setup(
    name="cosine_utils",
    version="0.1.2",
    description="A package to compute cosine similarity between vectors",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/cosine_utils",
    ext_modules=cythonize(extensions),  # Cythonize the extensions
    packages=["cosine_utils"],  # This includes the cosine_utils package
    install_requires=["numpy", "cython"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)
