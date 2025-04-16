from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="colour-image-toolbox",
    version="0.0.3",
    author="Miaosen Zhou",
    author_email="jackchou00@zju.edu.cn",
    description="A toolbox for image processing and analysis, specifically in colour science.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["colimage"],
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "colour-science",
    ],
    python_requires=">=3.12",
)
