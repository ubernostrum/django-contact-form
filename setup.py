import os

from setuptools import find_packages, setup


setup(
    name="django-contact-form",
    version="1.9",
    zip_safe=False,  # eggs are the devil.
    description="A generic contact-form application for Django",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    author="James Bennett",
    author_email="james@b-list.org",
    url="https://github.com/ubernostrum/django-contact-form/",
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    keywords=["django", "email", "contact-form"],
    python_requires=">=3.6",
    install_requires=["Django>=2.2,!=3.0.*"],
    extras_require={"akismet": ["akismet"]},
)
