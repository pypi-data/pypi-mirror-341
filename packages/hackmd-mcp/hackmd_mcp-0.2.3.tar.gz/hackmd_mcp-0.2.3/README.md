# HackMD MCP

HackMD MCP 是一個命令行工具和 MCP 服務，用於與 HackMD API 交互。

## 安裝

```bash
# 從 GitHub 安裝
git clone https://github.com/yourusername/hackmd-mcp.git
cd hackmd-mcp
pip install -e .

# 或從 PyPI 安裝（如果已發布）
pip install hackmd-mcp
```

## 設置

使用前需設定 HackMD API 令牌：

```bash
export HACKMD_API_TOKEN=您的API令牌
```

## 使用方法

### 基本命令

```bash
# 顯示幫助信息
hackmd-mcp --help

# 列出所有筆記
hackmd-mcp list

# 獲取筆記
hackmd-mcp get 筆記ID

# 創建筆記
hackmd-mcp create --title "標題" --content "內容" --tag 標籤1 --tag 標籤2

# 更新筆記
hackmd-mcp update 筆記ID --title "新標題" --content "新內容"

# 刪除筆記
hackmd-mcp delete 筆記ID

# 搜尋筆記
hackmd-mcp search 關鍵詞
```

### 作為 MCP 服務運行

```bash
# 啟動 HackMD MCP 服務
hackmd-mcp server
```

## 作者

Oliver

## 授權

MIT
