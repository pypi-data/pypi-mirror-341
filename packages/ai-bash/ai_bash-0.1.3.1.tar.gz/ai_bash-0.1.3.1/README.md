# AI-Bash: 智能命令行工具
# AI-Bash: Intelligent Command Line Tool

一个基于大模型的命令行工具，可以将自然语言需求转换为对应平台的命令行命令。
A command-line tool based on large language models that converts natural language requirements into platform-specific command line commands.

## 功能介绍
## Features

- 接收用户的自然语言描述
- Receive natural language descriptions from users
- 调用大模型API将需求转换为命令行命令
- Convert requirements into command line commands using LLM API
- 自动识别用户的操作系统和命令行环境
- Automatically detect user's operating system and command line environment
- 根据当前平台生成最适合的命令
- Generate the most suitable commands for the current platform
- 支持自定义API密钥、主机地址和模型名称
- Support custom API keys, host addresses, and model names
- 生成命令并在用户确认后执行
- Generate commands and execute after user confirmation
- 分析命令执行结果，提取有用信息
- Analyze command execution results and extract useful information

## 快速开始
## Quick Start

安装:
Installation:
```bash
uv tool install ai_bash
# 更新
# Update
uv tool upgrade ai-bash

```

使用:
Usage:
```bash
# 基本用法(生成命令并等待用户回车后执行)
# Basic usage (generate command and wait for user to press Enter)
ai 查一下当前目录的文件路径
ai check the file paths in current directory

# 只生成命令不执行
# Only generate command without execution
ai 列出所有进程 --no-exec
ai list all processes --no-exec

# 只输出纯文本命令，便于手动复制
# Output plain text command for manual copying
ai 查找大文件 --copy
ai find large files --copy

# 自动将命令复制到剪贴板，可直接粘贴使用
# Automatically copy command to clipboard for direct pasting
ai 查找大文件 --clipboard
ai find large files --clipboard

# 执行命令后交互式分析结果
# Interactive analysis after command execution
ai 获取最新10条git提交 --qa
ai get latest 10 git commits --qa

# 查看帮助信息
# View help information
ai --help
```

## 配置
## Configuration

初始化并查看配置:
Initialize and view configuration:
```bash
# 显示配置文件路径，如果不存在则创建
# Show config file path, create if not exists
ai --init

# 强制创建新配置文件(覆盖已有配置)
# Force create new config file (overwrite existing)
ai --init --force
```

配置文件位于用户主目录下的`.cmd_ai`文件:
Configuration file is located at `.cmd_ai` in user's home directory:
```
# 必需的API密钥
# Required API key
OPENAI_API_KEY=你的OpenAI API密钥
OPENAI_API_KEY=your OpenAI API key
```

## 交互式命令分析功能
## Interactive Command Analysis

使用`--qa` `-q` 选项来启用交互式命令分析功能:
Use `--qa` `-q` option to enable interactive command analysis:

```bash
# 执行git命令并进入交互式分析模式
# Execute git command and enter interactive analysis mode
ai 获取最近10次git提交日志 --qa
ai get latest 10 git commit logs --qa
```

执行命令后，工具会:
After command execution, the tool will:
1. 显示命令执行结果
   Show command execution results
2. 询问您是否需要AI分析结果
   Ask if you need AI analysis of the results
3. 如果需要，您可以输入具体的分析需求，例如：
   If needed, you can input specific analysis requirements, such as:
   - "总结最近的工作内容"
     "Summarize recent work"
   - "分析提交频率"
     "Analyze commit frequency"
   - "找出所有关于bug修复的提交"
     "Find all bug fix commits"
4. AI会根据您的需求分析命令输出
   AI will analyze command output according to your requirements
5. 分析完成后，还可以继续提出其他分析需求
   After analysis, you can continue to ask other analysis questions

## 文档与贡献
## Documentation and Contribution

- 详细使用说明和开发指南：[文档.md](文档.md)
  Detailed usage instructions and development guide: [文档.md](文档.md)
- 贡献代码规范：[CONTRIBUTING.md](CONTRIBUTING.md)
  Code contribution guidelines: [CONTRIBUTING.md](CONTRIBUTING.md) 