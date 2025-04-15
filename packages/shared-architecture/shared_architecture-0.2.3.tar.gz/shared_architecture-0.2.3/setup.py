from setuptools import setup, find_packages

setup(
    name="shared_architecture",  # Replace with your package name
    version="0.2.3",  # Increment version appropriately
    description="A shared library for backend services, including models, utilities, and configurations",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Raghuram Mutya",
    author_email="raghu.mutya@gmail.com",
    url="https://pypi.org/project/shared-models-stocksblitz/",  # Replace with your repository URL
    packages=find_packages(include=["shared_architecture", "shared_architecture.*"]),
    include_package_data=True,
    install_requires=[
        "SQLAlchemy>=1.4",
        "psycopg2>=2.9",
        "redis>=4.0",
        "pika>=1.3",
        "requests>=2.25",
        "pytest>=7.0",
        "pydantic>=1.10",
        "circuitbreaker>=1.3"
    ],
    python_requires=">=3.8",
    keywords="shared library architecture configuration connections enums backend",  # Add relevant keywords

)
