import re

from setuptools import find_packages, setup


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


EXTRAS_REQUIRE = {}
# EXTRAS_REQUIRE["tests"] = read("requirements/test.requirements.txt").splitlines()
# EXTRAS_REQUIRE["dev"] = read("requirements/dev.requirements.txt").splitlines()
REQUIRES = read("requirements/requirements.txt").splitlines()


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname) as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


setup(
    name="flask-mixins",
    version=find_version("src/flask_mixins/__init__.py"),
    description="Flask and marshmallow cleaner code",
    author="Tomas Sheers",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author_email="t.sheers@outlook.com",
    url="https://github.com/reritom/flask-mixins",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    license="MIT",
    zip_safe=False,
    keywords="flask-mixins",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    test_suite="tests",
    project_urls={
        "Issues": "https://github.com/reritom/flask-mixins/issues",
    },
)
