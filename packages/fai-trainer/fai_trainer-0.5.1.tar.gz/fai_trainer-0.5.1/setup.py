from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fai-trainer",
    version="0.5.1",
    author="Nizamuddin Mohamed & Michael Statelman",
    author_email="webnizam@gmail.com",
    description=
    "A package for training and testing image classification models using PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/webnizam/fai-trainer",
    packages=find_packages(),
    install_requires=[
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "Pillow>=8.0.0",
        "matplotlib>=3.3.0",
        "tqdm>=4.50.0",
        "numpy>=1.19.0",
        "scipy>=1.5.0",
        "scikit-learn>=0.23.2",
        "prettytable",
        "natsort",
        "fpdf",
    ],
    extras_require={
        "xpu": ["intel-extension-for-pytorch"],  # Optional Intel XPU support
    },
    entry_points={
        "console_scripts": [
            "fai-trainer=trainer.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
