from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below are parsed by `docs/conf.py`.
name = "oprf"
version = "2.0.0"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=["oblivious~=4.0.1",],
    license="MIT",
    url="https://github.com/nthparty/oprf",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Oblivious pseudo-random function (OPRF) protocol "+\
                "functionality implementations based on Curve25519 "+\
                "primitives.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
