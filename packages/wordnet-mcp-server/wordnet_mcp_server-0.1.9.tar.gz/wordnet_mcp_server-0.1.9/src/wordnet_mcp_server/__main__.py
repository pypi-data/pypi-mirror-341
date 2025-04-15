"""
WordNet MCP服务主入口

该文件允许将包作为Python模块直接运行：
python -m wordnet_mcp_server
"""

from .app import main

if __name__ == "__main__":
    main() 