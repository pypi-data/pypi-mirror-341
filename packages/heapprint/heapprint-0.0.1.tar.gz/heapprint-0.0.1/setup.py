from setuptools import setup, find_packages

setup(
    name="heapprint",
    version="0.0.1",
    packages=find_packages(),
    author="Jasur Omanov",
    description="Heap (ikkilik daraxt) tuzilishini vizual ko'rsatish uchun Python kutubxonasi",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)