<div align="center">

# 🔄 SyncPilot-CLI

**Lightweight Terminal File Synchronization & Backup Engine**

**轻量级终端智能文件同步与备份引擎**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**SyncPilot-CLI** is a lightweight, zero-dependency terminal file synchronization and backup engine designed for developers and system administrators who need fast, reliable, and intelligent file sync capabilities.

**Key Differentiators:**
- 🚀 **Zero Dependencies** - Uses only Python standard library
- ⚡ **Incremental Sync** - Hash-based change detection for efficient transfers
- 📸 **Snapshot Management** - Version control for your files
- 🎨 **TUI Dashboard** - Beautiful terminal interface with progress bars
- 🔒 **Safe by Default** - Dry-run mode and conflict detection

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📥 **Incremental Sync** | Only syncs changed files based on hash comparison |
| 🔄 **Bidirectional Sync** | Two-way synchronization with conflict resolution |
| 📸 **Snapshot System** | Create and restore file snapshots anytime |
| 🎯 **Smart Filtering** | .gitignore-style pattern matching |
| 📊 **Progress Tracking** | Real-time progress bars and statistics |
| 🔍 **Dry Run Mode** | Preview changes before executing |
| ⚡ **High Performance** | Multi-threaded scanning and copying |
| 🌍 **Cross-Platform** | Works on Windows, macOS, and Linux |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- No external dependencies required!

#### Installation

**Method 1: Direct Download**
```bash
curl -O https://raw.githubusercontent.com/gitstq/SyncPilot-CLI/main/syncpilot.py
chmod +x syncpilot.py
```

**Method 2: Clone Repository**
```bash
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI
python3 syncpilot.py --version
```

**Method 3: pip Install**
```bash
pip install -e .
# Now you can use 'syncpilot' or 'sp' command globally
```

#### Basic Usage

```bash
# Sync two directories
syncpilot sync ./source ./backup

# Preview changes without executing (dry-run)
syncpilot sync ./source ./backup --dry-run

# Sync and delete extra files in target
syncpilot sync ./source ./backup --delete

# Create a snapshot
syncpilot snapshot ./important-files --name "before-update"

# List all snapshots
syncpilot snapshot ./important-files --list

# Compare two directories
syncpilot compare ./source ./backup
```

### 📖 Detailed Usage Guide

#### Sync Command

```bash
syncpilot sync [OPTIONS] SOURCE TARGET

Options:
  --dry-run         Preview mode (no actual changes)
  --delete          Delete extra files in target
  --ignore-file     Custom ignore pattern file (default: .syncignore)
  --no-hash         Disable file hash comparison
  -v, --verbose     Detailed output
  -q, --quiet       Silent mode
```

#### Snapshot Command

```bash
# Create snapshot
syncpilot snapshot ./my-project --name "v1.0-release"

# List snapshots
syncpilot snapshot ./my-project --list

# Load snapshot info
syncpilot snapshot ./my-project --load "v1.0-release"
```

#### Compare Command

```bash
syncpilot compare ./source ./target
```

Output shows:
- Files only in source
- Files only in target
- Different files
- Identical files

### 💡 Design Philosophy

**Why SyncPilot?**

1. **Simplicity** - Single-file implementation, easy to understand and modify
2. **Zero Dependencies** - No pip install hell, works on any Python 3.8+ system
3. **Intelligence** - Smart change detection minimizes unnecessary transfers
4. **Safety** - Dry-run mode and confirmation prompts prevent accidents
5. **Visibility** - Beautiful TUI with real-time progress tracking

**Technical Highlights:**
- Uses MD5/SHA256 hashing for accurate change detection
- Multi-threaded file scanning for better performance
- JSON-based snapshot format for portability
- Modular architecture for easy extension

### 📦 Packaging & Deployment

#### Build from Source

```bash
# Clone repository
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI

# Install in development mode
pip install -e .

# Or run directly
python3 syncpilot.py --help
```

#### Create Standalone Executable

```bash
# Install pyinstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name syncpilot syncpilot.py

# Find executable in dist/ directory
./dist/syncpilot --version
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**SyncPilot-CLI** 是一款轻量级、零依赖的终端文件同步与备份引擎，专为需要快速、可靠、智能文件同步功能的开发者和系统管理员设计。

**核心差异化亮点：**
- 🚀 **零依赖** - 仅使用 Python 标准库
- ⚡ **增量同步** - 基于哈希的变更检测，高效传输
- 📸 **快照管理** - 文件版本控制，随时回滚
- 🎨 **TUI 仪表盘** - 美观的终端界面，实时进度条
- 🔒 **安全优先** - 支持试运行模式和冲突检测

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📥 **增量同步** | 仅同步基于哈希比较发生变化的文件 |
| 🔄 **双向同步** | 支持双向同步与冲突解决 |
| 📸 **快照系统** | 随时创建和恢复文件快照 |
| 🎯 **智能过滤** | 支持 .gitignore 风格的模式匹配 |
| 📊 **进度追踪** | 实时进度条和统计信息 |
| 🔍 **试运行模式** | 执行前预览所有变更 |
| ⚡ **高性能** | 多线程扫描和复制 |
| 🌍 **跨平台** | 支持 Windows、macOS 和 Linux |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- 无需任何外部依赖！

#### 安装方法

**方式一：直接下载**
```bash
curl -O https://raw.githubusercontent.com/gitstq/SyncPilot-CLI/main/syncpilot.py
chmod +x syncpilot.py
```

**方式二：克隆仓库**
```bash
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI
python3 syncpilot.py --version
```

**方式三：pip 安装**
```bash
pip install -e .
# 现在可以全局使用 'syncpilot' 或 'sp' 命令
```

#### 基础用法

```bash
# 同步两个目录
syncpilot sync ./source ./backup

# 预览变更（不实际执行）
syncpilot sync ./source ./backup --dry-run

# 同步并删除目标目录中的多余文件
syncpilot sync ./source ./backup --delete

# 创建快照
syncpilot snapshot ./important-files --name "update-before"

# 列出所有快照
syncpilot snapshot ./important-files --list

# 比较两个目录
syncpilot compare ./source ./backup
```

### 📖 详细使用指南

#### 同步命令

```bash
syncpilot sync [选项] 源目录 目标目录

选项：
  --dry-run         试运行模式（不实际变更）
  --delete          删除目标目录中的多余文件
  --ignore-file     自定义忽略模式文件（默认：.syncignore）
  --no-hash         禁用文件哈希比较
  -v, --verbose     详细输出
  -q, --quiet       静默模式
```

#### 快照命令

```bash
# 创建快照
syncpilot snapshot ./my-project --name "v1.0-release"

# 列出快照
syncpilot snapshot ./my-project --list

# 加载快照信息
syncpilot snapshot ./my-project --load "v1.0-release"
```

#### 比较命令

```bash
syncpilot compare ./source ./target
```

输出包含：
- 仅在源目录中的文件
- 仅在目标目录中的文件
- 不同的文件
- 相同的文件

### 💡 设计思路

**为什么选择 SyncPilot？**

1. **简洁** - 单文件实现，易于理解和修改
2. **零依赖** - 无需 pip 安装，在任何 Python 3.8+ 系统上运行
3. **智能** - 智能变更检测，最小化不必要的传输
4. **安全** - 试运行模式和确认提示，防止误操作
5. **可视化** - 美观的 TUI 界面，实时进度追踪

**技术亮点：**
- 使用 MD5/SHA256 哈希进行精确的变更检测
- 多线程文件扫描提升性能
- JSON 格式的快照，便于移植
- 模块化架构，易于扩展

### 📦 打包与部署

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI

# 开发模式安装
pip install -e .

# 或直接运行
python3 syncpilot.py --help
```

#### 创建独立可执行文件

```bash
# 安装 pyinstaller
pip install pyinstaller

# 构建可执行文件
pyinstaller --onefile --name syncpilot syncpilot.py

# 在 dist/ 目录找到可执行文件
./dist/syncpilot --version
```

### 🤝 贡献指南

欢迎贡献代码！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 
<a name="繁體中文"></a>
## 🇹
<a name="繁體中文"></a>
## 🇹

### 🎉 專案介紹

**SyncPilot-CLI** 是一款輕量級、零依賴的終端機檔案同步與備份引擎，專為需要快速、可靠、智慧檔案同步功能的開發者和系統管理員設計。

**核心差異化亮點：**
- 🚀 **零依賴** - 僅使用 Python 標準庫
- ⚡ **增量同步** - 基於雜湊的變更檢測，高效傳輸
- 📸 **快照管理** - 檔案版本控制，隨時回滾
- 🎨 **TUI 儀表板** - 美觀的終端機介面，即時進度條
- 🔒 **安全優先** - 支援試執行模式和衝突檢測

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📥 **增量同步** | 僅同步基於雜湊比較發生變化的檔案 |
| 🔄 **雙向同步** | 支援雙向同步與衝突解決 |
| 📸 **快照系統** | 隨時建立和恢復檔案快照 |
| 🎯 **智慧過濾** | 支援 .gitignore 風格的模式匹配 |
| 📊 **進度追蹤** | 即時進度條和統計資訊 |
| 🔍 **試執行模式** | 執行前預覽所有變更 |
| ⚡ **高效能** | 多執行緒掃描和複製 |
| 🌍 **跨平臺** | 支援 Windows、macOS 和 Linux |

### 🚀 快速開始

#### 環境要求
- Python 3.8 或更高版本
- 無需任何外部依賴！

#### 安裝方法

**方式一：直接下載**
```bash
curl -O https://raw.githubusercontent.com/gitstq/SyncPilot-CLI/main/syncpilot.py
chmod +x syncpilot.py
```

**方式二：克隆倉庫**
```bash
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI
python3 syncpilot.py --version
```

**方式三：pip 安裝**
```bash
pip install -e .
# 現在可以全域性使用 'syncpilot' 或 'sp' 命令
```

#### 基礎用法

```bash
# 同步兩個目錄
syncpilot sync ./source ./backup

# 預覽變更（不實際執行）
syncpilot sync ./source ./backup --dry-run

# 同步並刪除目標目錄中的多餘檔案
syncpilot sync ./source ./backup --delete

# 建立快照
syncpilot snapshot ./important-files --name "update-before"

# 列出所有快照
syncpilot snapshot ./important-files --list

# 比較兩個目錄
syncpilot compare ./source ./backup
```

### 📖 詳細使用指南

#### 同步命令

```bash
syncpilot sync [選項] 源目錄 目標目錄

選項：
  --dry-run         試執行模式（不實際變更）
  --delete          刪除目標目錄中的多餘檔案
  --ignore-file     自定義忽略模式檔案（預設：.syncignore）
  --no-hash         禁用檔案雜湊比較
  -v, --verbose     詳細輸出
  -q, --quiet       靜默模式
```

#### 快照命令

```bash
# 建立快照
syncpilot snapshot ./my-project --name "v1.0-release"

# 列出快照
syncpilot snapshot ./my-project --list

# 載入快照資訊
syncpilot snapshot ./my-project --load "v1.0-release"
```

#### 比較命令

```bash
syncpilot compare ./source ./target
```

輸出包含：
- 僅在源目錄中的檔案
- 僅在目標目錄中的檔案
- 不同的檔案
- 相同的檔案

### 💡 設計思路

**為什麼選擇 SyncPilot？**

1. **簡潔** - 單檔案實現，易於理解和修改
2. **零依賴** - 無需 pip 安裝，在任何 Python 3.8+ 系統上執行
3. **智慧** - 智慧變更檢測，最小化不必要的傳輸
4. **安全** - 試執行模式和確認提示，防止誤操作
5. **視覺化** - 美觀的 TUI 介面，即時進度追蹤

**技術亮點：**
- 使用 MD5/SHA256 雜湊進行精確的變更檢測
- 多執行緒檔案掃描提升效能
- JSON 格式的快照，便於移植
- 模組化架構，易於擴充套件

### 📦 打包與部署

#### 從原始碼構建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/SyncPilot-CLI.git
cd SyncPilot-CLI

# 開發模式安裝
pip install -e .

# 或直接執行
python3 syncpilot.py --help
```

#### 建立獨立可執行檔案

```bash
# 安裝 pyinstaller
pip install pyinstaller

# 構建可執行檔案
pyinstaller --onefile --name syncpilot syncpilot.py

# 在 dist/ 目錄找到可執行檔案
./dist/syncpilot --version
```

### 🤝 貢獻指南

歡迎貢獻程式碼！請隨時提交 Pull Request。

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。
