from setuptools import setup, find_packages

setup(
  name="opensfc",
  version="0.0.1",
  author="Coleman Ammerman",
  author_email="colemanra3@ReedWare.com",
  description="OpenSFC is a visual, high-level automation system using flowcharts.",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://OpenSFC.com",
  packages=find_packages(),
  python_requires=">=3.7",
  license="AGPL-3.0-or-later",
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
)
