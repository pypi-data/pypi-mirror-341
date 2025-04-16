from setuptools import setup, find_packages

# with open("requirements.txt") as f:
#     requirements = f.read().splitlines()

setup(
    name='llumo',
    version='0.1.1',
    description='Python SDK for interacting with the Llumo ai API.',
    author='Llumo',
    author_email='product@llumo.ai',
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "setuptools>=58.1.0",
        "twine>=6.1.0",
        "wheel>=0.45.1",
        "build>=1.2.2.post1"],
    python_requires='>=3.7',
    include_package_data=True,
    url="https://www.llumo.ai/",
    license='Proprietary'

    
)
