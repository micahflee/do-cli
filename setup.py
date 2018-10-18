import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="do-cli",
    version="0.1.0",
    author="Micah Lee",
    author_email="micah@micahflee.com",
    description="A simple command line tool for listing, creating, and deleting DigitalOcean droplets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    python_requires=">=3.4",
    url="https://github.com/micahflee/do",
    scripts=['do'],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Internet"
    ),
    install_requires=['colored', 'tabulate', 'dopy']
)
