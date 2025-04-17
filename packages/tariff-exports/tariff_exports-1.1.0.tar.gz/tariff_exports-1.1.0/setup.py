from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tariff-exports",
    version="1.1.0",
    author="Python Economist",
    author_email="eterna2@hotmail.com",
    description="Make importing great again! A parody package that imposes tariffs on Python imports. Extended to include tariffs on Python exports too.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/e2forks/tariff",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    keywords="import, tariff, parody, monkey-patch",
)
