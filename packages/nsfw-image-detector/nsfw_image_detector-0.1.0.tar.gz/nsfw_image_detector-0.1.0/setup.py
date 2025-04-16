from setuptools import setup, find_packages

setup(
    name="nsfw_image_detector",
    version="0.1.0",
    description="A Python package for NSFW image detection using EVA-based vision transformer",
    author="Freepik",
    author_email="info@freepik.com",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "Pillow>=9.0.0",
        "timm>=0.6.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
) 