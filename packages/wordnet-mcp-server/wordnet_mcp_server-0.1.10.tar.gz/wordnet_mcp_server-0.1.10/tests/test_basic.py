"""
基本测试
"""

import pytest
from wordnet_mcp_server import __version__

def test_version():
    """测试版本号格式是否正确"""
    assert __version__, "版本号不应为空"
    assert isinstance(__version__, str), "版本号应为字符串"
    assert len(__version__.split(".")) == 3, "版本号应符合语义版本格式 x.y.z" 