from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="oprf",
    version="0.1.0",
    packages=["oprf",],
    install_requires=["oblivious",],
    license="MIT",
    url="https://github.com/nthparty/oprf",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Oblivious pseudo-random function (OPRF) protocol "+\
                "functionality implementations based on Ed25519 primitives.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
