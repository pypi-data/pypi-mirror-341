# Volcengine MCP

Volcengine VOD 的 Model Context Protocol (MCP) Server 实现

## 项目简介

Volcengine VOD MCP是一个基于[Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)的 MCP-server，
它将 Volcengine VOD服务集成到LLM模型上下文中，使大模型能够直接操作和管理VOD资源。

## 功能特点

- 提供多种资源访问接口，便于LLM获取Volcengine VOD服务信息
- 实现了多个Volcengine功能的工具封装，包括上传媒资，剪辑视频等

## 安装

### 环境要求

- Python 3.11+
- 火山引擎账号及AccessKey/SecretKey

### 安装依赖

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 使用方法

### 在 Mcp Client 中集成

在 mcp client 中配置 mcp 服务, (还没有发布包 暂时用 sh命令 运行 server 脚本，后续如果发布包 则用 uvx 运行 server 脚本)， 配置的 MCP JSON：

```json
{
  "mcpServers": {
    "vevod": {
      "command": "sh",
      "args": ["/{your_path}/mcp-vod/scripts/run.sh"],
      "vevod": {
        "env": {
          "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
          "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
        }
      }
    }
  }
}
```

请在[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)申请ACCESS_KEY、SECRET_KEY

### 使用 @modelcontextprotocol/inspector 调试

```bash
sh ./scripts/debug.sh
```