# WordNet MCP 服务

这是一个基于WordNet的Model Context Protocol (MCP) 服务实现，提供词汇查询功能，包括同义词、反义词、上下位词和定义等。

## 项目地址

GitHub: [github.com/keepondream/wordnet-mcp-server](https://github.com/keepondream/wordnet-mcp-server)

## 功能

- 查询单词的同义词
- 查询单词的反义词
- 查询单词的上位词（更一般的概念）
- 查询单词的下位词（更具体的概念）
- 查询单词的定义和例句
- 获取单词的综合信息

## 安装

### 通过 PyPI 安装

推荐使用 [uv](https://github.com/astral-sh/uv) 安装:

```bash
# 安装 wordnet-mcp-server
uvx wordnet-mcp-server
```

或者使用 pip:

```bash
# 安装 wordnet-mcp-server
pip install wordnet-mcp-server
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/keepondream/wordnet-mcp-server.git
cd wordnet-mcp-server

# 安装依赖和项目
uv pip install -e .
```

## 使用方法

### 直接运行

安装后，可以直接使用命令行运行服务:

```bash
# 使用入口点运行
wordnet-mcp

# 或者使用 Python 模块运行
python -m wordnet_mcp_server
```

### 在 MCP 客户端中配置服务

#### 方法一：直接使用 uvx 命令（推荐）

当服务发布到 PyPI 后，您可以直接使用 uvx 命令配置（最简单的方式）：

```json
{
  "mcpServers": {
    "wordnet": {
      "command": "uvx",
      "args": ["wordnet-mcp-server"]
    }
  }
}
```

#### 方法二：指定 Python 解释器和模块路径

```json
{
  "mcpServers": {
    "WordNet MCP": {
      "command": "python3",
      "type": "stdio",
      "args": ["-m", "wordnet_mcp_server"]
    }
  }
}
```

#### 在 Cursor 中添加 MCP 服务

1. 在 Cursor 中安装 MCP 服务
2. 添加 WordNet MCP 服务（使用上述配置方式之一）
3. 在使用时，可以选择所需的功能进行调用

## 示例

### 代码示例

```python
# 查询单词 "happy" 的同义词
get_synonyms("happy")

# 查询单词 "happy" 的反义词
get_antonyms("happy")

# 获取单词 "happy" 的所有相关信息
get_word_info("happy")
```

### 在LLM对话中使用示例

配置好MCP服务后，您可以在与Claude、GPT等支持MCP的LLM对话时使用这些工具。以下是一些对话示例：

#### 示例1：查询单词同义词

**用户**: 请帮我查找单词"improve"的同义词。

**LLM**: 我会使用WordNet工具查询"improve"的同义词。

_[LLM调用get_synonyms工具]_

"improve"的同义词包括：
- enhance
- ameliorate
- better
- meliorate
- advance
- improve upon
- improve on
...

#### 示例2：获取单词的反义词

**用户**: "success"的反义词有哪些？

**LLM**: 让我查询"success"的反义词。

_[LLM调用get_antonyms工具]_

"success"的反义词包括：
- failure
- unsuccess
- ...

#### 示例3：理解概念层次关系

**用户**: 我想了解"dog"在生物分类中的上位概念和下位概念。

**LLM**: 我会分别查询"dog"的上位词（更一般的概念）和下位词（更具体的概念）。

_[LLM调用get_hypernyms和get_hyponyms工具]_

"dog"的上位概念包括：
- canine
- domestic animal
- carnivore
- mammal
...

"dog"的下位概念包括：
- puppy
- pooch
- hound
- poodle
- terrier
- retriever
...

#### 示例4：查询综合信息

**用户**: 请给我详细介绍单词"time"的各种含义。

**LLM**: 我将查询"time"的综合信息。

_[LLM调用get_word_info工具]_

"time"的信息如下：

**同义词**:
- time period
- period of time
- period
...

**定义**:
1. a nonspatial continuum in which events occur in apparently irreversible succession
2. a quantity representing duration
3. an instance or occasion
...

**例句**:
- "they were living in a time of great social change"
- "he was a great actor in his time"
...

## 开发

### 安装开发依赖

```bash
# 安装开发依赖
uv pip install -e ".[dev]"
```

### 使用 Makefile

项目提供了Makefile，可以轻松进行开发和发布操作：

```bash
# 递增版本号
make bump-version

# 构建包
make build

# 发布到PyPI
make publish

# 本地安装
make install

# 运行测试
make test

# 清理构建文件
make clean
``` 