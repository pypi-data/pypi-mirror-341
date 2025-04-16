from setuptools import setup, find_packages

setup(
    name="socketnest",
    version="0.1.0",
    description="SocketNest Server Python Library",
    author="Daniel Mendoza",
    author_email="daniel@socketnest.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"socketnest": ["__init__.py"]},
    install_requires=[
        "requests>=2.0.0"
    ],
    tests_require=[
        "pytest>=7.0"
    ],
    python_requires=">=3.7,<4.0",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/socketnest/socketnest-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
