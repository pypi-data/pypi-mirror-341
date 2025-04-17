# Cursor中连接知网搜索MCP服务器指南

本指南提供在Cursor中成功连接到知网搜索MCP服务器的详细步骤。

## 准备工作

1. 确保已正确安装Python 3.10或更高版本
2. 安装最新版本的MCP：
   ```bash
   uv add "mcp[cli]" --upgrade
   ```
3. 确保Chrome浏览器已安装
4. 安装Playwright（推荐）：
   ```bash
   # 安装playwright库
   uv add playwright
   
   # 安装playwright浏览器
   playwright install
   ```

## 启动服务器

在终端中运行以下命令启动服务器：

```bash
# 进入项目目录
cd 你的项目路径/kwds2rslt/cnks

# 启动服务器
python -m cnks
```

如果一切正常，你应该看到：
```
启动知网搜索FastMCP服务器...
```

保持此终端窗口开启。

## 在Cursor中连接

1. 打开Cursor
2. 点击右下角的"Claude"图标
3. 选择"Connect to MCP Server"
4. 选择"Subprocess (stdio)"连接方式
5. 在命令输入框中输入：
   ```
   python -m cnks
   ```
6. 点击"Connect"

成功连接后，你会看到Claude提示已连接到知网搜索服务器。

## 测试连接

连接成功后，尝试以下指令测试服务器功能：

```
请打开中国知网搜索页面
```

如果Chrome浏览器成功打开中国知网页面，则表示连接成功。

然后测试搜索功能：

```
请在知网搜索"预印本"相关论文
```

如果安装了Playwright，应该会看到浏览器自动在搜索框中输入"预印本"并执行搜索。
如果没有安装Playwright，只会打开知网页面而不会自动输入搜索词。

## 故障排除

如果无法连接，请尝试以下步骤：

### 1. 检查服务器状态

确保服务器正在运行且没有错误消息。尝试重启服务器：

```bash
# 按Ctrl+C终止当前服务器
# 然后重新启动
python -m cnks
```

### 2. 使用开发模式测试

使用MCP开发模式直接测试服务器是否正常工作：

```bash
mcp dev src/cnks/server.py
```

如果开发模式可以正常工作但Cursor无法连接，则问题可能在连接配置上。

### 3. 检查Chrome路径

如果服务器报告找不到Chrome，设置环境变量指定Chrome路径：

```bash
# Windows
set CHROME_PATH="C:\你的Chrome路径\chrome.exe"

# macOS/Linux
export CHROME_PATH="/path/to/chrome"
```

### 4. Playwright问题

如果使用Playwright时遇到问题：

```bash
# 验证playwright是否已安装
uv pip show playwright

# 重新安装
uv add playwright --upgrade

# 安装浏览器
playwright install
```

如果安装浏览器时遇到权限问题，可能需要以管理员身份运行命令。

### 5. 使用直接路径

如果连接依然失败，尝试在Cursor中提供服务器脚本的完整路径：

```
python C:/你的项目完整路径/kwds2rslt/cnks/src/cnks/server.py
```

### 6. 检查防火墙和安全软件

确保没有防火墙或安全软件阻止进程间通信。

### 7. 更新MCP和Cursor

确保使用最新版本的MCP库和Cursor应用。

## 获取更多帮助

如果以上方法都无法解决问题，请：

1. 查看完整的错误消息和服务器日志
2. 在GitHub上提交问题，附上完整的错误信息和环境详情 