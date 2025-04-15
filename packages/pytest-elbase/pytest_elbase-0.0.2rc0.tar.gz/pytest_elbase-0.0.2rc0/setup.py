from setuptools import setup
import pathlib

long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(encoding="utf-8")

setup(
    name="pytest-elbase",
    version="0.0.2rc0",
    description="Elbase pytest plugin",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://elbase.io",
    author="Elbase Packaging",
    author_email="pkg@elbase.io",
    python_requires=">=3.7, <4",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["pytest_elbase"],
    project_urls={
        "Documentation": "https://docs.elbase.io",
    },
)
