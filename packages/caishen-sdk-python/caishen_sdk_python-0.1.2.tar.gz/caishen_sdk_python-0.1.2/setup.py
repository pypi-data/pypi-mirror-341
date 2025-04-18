from setuptools import setup, find_packages

setup(
    name="caishen_sdk_python",
    version="0.1.2",
    description="The Caishen SDK gives every agent or user access to unlimited multi-chain crypto wallets",
    author="CaishenTech",
    author_email="hello@caishen.tech",
    url="https://github.com/CaishenTech/caishen_sdk_python/",  # Update with your URL or repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
