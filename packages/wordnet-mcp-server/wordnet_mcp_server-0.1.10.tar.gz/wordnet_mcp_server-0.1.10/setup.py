#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个文件是为了向后兼容性保留的。
实际的项目配置在pyproject.toml中。
"""

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
    ) 