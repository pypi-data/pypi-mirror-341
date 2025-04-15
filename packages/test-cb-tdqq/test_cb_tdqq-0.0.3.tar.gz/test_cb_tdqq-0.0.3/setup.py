from setuptools import setup, find_packages

setup(
    name="test-cb-tdqq",
    version="0.0.3",
    packages=find_packages(),
    install_requires=["pandas >= 2.2.3",
                      "numpy >= 1.26.4",
                      "torch >= 2.4.1",
                      "transformers >= 4.44.2",
                      "sentence-transformers >= 3.2.0",
                      "faiss-cpu >= 1.10.0",
                      "rank-bm25 >= 0.2.2",
                      "stop-words == 2018.7.23"],
    extras_require={
        "gpu": ["faiss-gpu >= 1.7.2"],
    },
    author="Thuong Dang, Qiqi Chen",
    author_email="dangtuanthuong@gmail.com",
    description="Simple test package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    license_files=['LICENSE'],
    license='MIT',
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
