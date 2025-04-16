#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ksiterate",
	version="1.2",
	author="Konrad Sakowski",
	description="Module for iteration over product of given parameter values",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
	],
	platforms = ["any", ],
	python_requires='>=3.6',
	py_modules=["ksiterate"],
	package_dir={'':'ksiterate/src'},
	install_requires=[]
)
