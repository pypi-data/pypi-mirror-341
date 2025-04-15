from setuptools import setup, find_packages

with open ("README.md", "r") as f:
		page_description = f.read()

with open ("requirements.txt") as f:
		requirements = f.read().splitlines()
		
setup(
	name= "dedessa-image-processing",
	version="0.0.1",
	author="Andressa",
	author_email="andressa_rtlas@hotmail.com",
	description="Implematation of image processing",
	long_description=page_description,
	long_description_content_type="text/markdown",
	url="https://github.com/notdessa/image-processing-package.git",
	packages=find_packages(),
	classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
	install_requires=requirements,
	python_requires='>=3',
)