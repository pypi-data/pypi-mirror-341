from setuptools import setup, find_packages

setup(
    name="utm-tracker-django",
    version="1.0",
    description="Middleware to track UTM parameters in Django",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Preet Sonpal",
    author_email="preet@weirdlabs.in",
    url="https://github.com/yourusername/django-utm-tracker",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[],
)
