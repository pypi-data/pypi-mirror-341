from setuptools import setup, find_packages


setup(
    name="colour-image-toolbox",
    version="0.0.2",
    author="Miaosen Zhou",
    author_email="jackchou00@zju.edu.cn",
    description="A toolbox for image processing and analysis, specifically in colour science.",
    packages=["colimage"],
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "colour-science",
    ],
    python_requires=">=3.12",
)
