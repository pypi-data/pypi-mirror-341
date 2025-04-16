# 微博热搜 MCP Server

这是一个基于 FastMCP 框架的微博热搜数据获取服务器，提供了获取微博热搜榜、热搜详情和评论等功能。

## 功能特性

1. 获取微博热搜榜单
   - 展示热搜排名
   - 显示热搜词
   - 显示热搜指数

2. 获取热搜详细信息
   - 话题分类
   - 话题描述
   - 话题链接
   - 话题主持人信息
   - 统计数据（阅读量、讨论量、互动量、原创量）

3. 获取热搜评论
   - 支持通过 URL 获取评论
   - 可配置最大评论获取数量
   - 显示评论内容和点赞数

## 安装要求

- Python 3.x
- 依赖包：
  - requests
  - lxml
  - mcp

## 安装步骤

1. 克隆仓库到本地
2. 安装依赖：
```bash
pip install requests lxml fastmcp
```

## 使用方法

### 启动服务器
```bash
python server.py
```

服务器将以 stdio 模式运行，可以通过 FastMCP 客户端进行调用。

## API 说明

服务器提供以下 MCP 工具：

### 1. get_hot_search
获取微博热搜榜单
```python
# MCP 调用示例
result = await mcp.call("get_hot_search", {})
```

### 2. get_hot_search_detail
获取指定话题的详细信息
```python
# MCP 调用示例
result = await mcp.call("get_hot_search_detail", {
    "word": "话题关键词"
})
```

### 3. get_hot_search_comment_by_url
获取指定话题的评论
```python
# MCP 调用示例
result = await mcp.call("get_hot_search_comment_by_url", {
    "cookie": "你的微博cookie",
    "url": "话题链接",
    "max_comments": 40  # 可选，默认40条，最大200条
})
```

## 注意事项

1. 获取评论功能需要提供有效的微博 cookie
2. 评论获取数量上限为 200 条
3. 部分热搜话题可能无法获取详细信息
4. 建议合理控制接口调用频率，避免被限制
5. 服务器使用 stdio 传输模式，需要通过 FastMCP 客户端调用

## 技术说明

- 使用 FastMCP 框架构建服务器
- 采用 requests 库进行 HTTP 请求
- 使用 lxml 解析网页内容
- 支持异步操作和异常处理
- 使用 stdio 作为传输层

## 许可证

[根据实际情况填写许可证信息] 