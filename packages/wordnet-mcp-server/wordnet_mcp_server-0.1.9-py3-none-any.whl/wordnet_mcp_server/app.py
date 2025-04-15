import nltk
from nltk.corpus import wordnet as wn
from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务器
mcp = FastMCP("WordNet MCP")

# 确保WordNet数据已下载
def download_wordnet():
    nltk.download('wordnet')

# 下载所需数据
download_wordnet()

@mcp.tool()
def get_synonyms(word: str) -> list[str]:
    """获取给定单词的同义词列表"""
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

@mcp.tool()
def get_antonyms(word: str) -> list[str]:
    """获取给定单词的反义词列表"""
    antonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                antonyms.add(antonym.name().replace('_', ' '))
    return list(antonyms)

@mcp.tool()
def get_hypernyms(word: str) -> list[str]:
    """获取给定单词的上位词（更一般的概念）"""
    hypernyms = set()
    for syn in wn.synsets(word):
        for hypernym in syn.hypernyms():
            hypernyms.add(hypernym.name().split('.')[0].replace('_', ' '))
    return list(hypernyms)

@mcp.tool()
def get_hyponyms(word: str) -> list[str]:
    """获取给定单词的下位词（更具体的概念）"""
    hyponyms = set()
    for syn in wn.synsets(word):
        for hyponym in syn.hyponyms():
            hyponyms.add(hyponym.name().split('.')[0].replace('_', ' '))
    return list(hyponyms)

@mcp.tool()
def get_definition(word: str) -> list[dict]:
    """获取给定单词的所有定义"""
    definitions = []
    for syn in wn.synsets(word):
        definitions.append({
            "pos": syn.pos(),
            "definition": syn.definition(),
            "examples": syn.examples()
        })
    return definitions

@mcp.tool()
def get_word_info(word: str) -> dict:
    """获取单词的综合信息（同义词、反义词、定义等）"""
    return {
        "synonyms": get_synonyms(word),
        "antonyms": get_antonyms(word),
        "hypernyms": get_hypernyms(word),
        "hyponyms": get_hyponyms(word),
        "definitions": get_definition(word)
    }

def main():
    """命令行入口点，用于通过uvx命令启动服务"""
    # 确保WordNet数据已下载
    download_wordnet()
    # 启动MCP服务
    mcp.run()

if __name__ == "__main__":
    # 启动MCP服务
    main() 