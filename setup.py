#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = "cftool",
        version = "0.2",
        author = "AnotherTwinkle",
        url = "https://www.github.com/AnotherTwinkle/cftool",
        packages = find_packages(),
        include_package_data = True,
        entry_points = {'console_scripts' : ['cftool=cftool.main:main']}
        )
        
