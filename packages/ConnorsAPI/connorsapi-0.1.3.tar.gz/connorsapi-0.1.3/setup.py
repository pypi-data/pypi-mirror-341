from setuptools import setup, find_packages

setup(
    name="ConnorsAPI",  # The name of your package
    version="0.1.3",
    packages=find_packages(),  # Automatically finds the 'api_thingy' directory
    install_requires=[  # Add any external libraries here
        # "requests",  # Example if you have any dependencies
    ],
    description="A short description of your package",
    author="Connor Daniels",
    author_email="youremail@example.com",
    url="https://github.com/Concon6321/API-THINGY",  # Your GitHub URL
    include_package_data=True,
)
