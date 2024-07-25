## 前端项目启动教程

### 1. 安装 Node.js 和 pnpm

确保你已经安装了 [Node.js](https://nodejs.org/) 和 [pnpm](https://pnpm.io/)。你可以通过以下命令检查安装情况：

```bash
node -v
pnpm -v
```

### 2. 克隆项目仓库

```bash
git clone https://gitee.com/lok666/ssq.git
cd https://gitee.com/lok666/ssq.git
```

### 3. 安装前端依赖

```bash
pnpm install
```

### 4. 启动前端开发服务器

```bash
pnpm run dev
```

## 后端 FastAPI 项目启动教程

### 1. 安装 Python 3.10

确保你已经安装了 [Python 3.10](https://www.python.org/downloads/)。你可以通过以下命令检查安装情况：

```bash
python --version
```

### 2. 创建虚拟环境

在项目根目录下创建一个虚拟环境：

```bash
python -m venv venv
```

激活虚拟环境：

- **Windows**：

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**：

  ```bash
  source venv/bin/activate
  ```

### 3. 安装后端依赖

在虚拟环境中安装依赖：

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

在你的代码中找到数据库配置部分，修改数据库密码等相关信息。例如，修改 `database.py` 中的配置：

```python
DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost/lottery"
```

### 5. 导入数据库文件

确保你已经安装了 MySQL。你可以通过以下命令检查安装情况：

```bash
mysql --version
```

创建数据库并导入 `lottery.sql` 文件：

```bash
mysql -u root -p
```

在 MySQL 命令行中：

```sql
CREATE DATABASE lottery;
USE lottery;
SOURCE /path/to/lottery.sql;
```

### 6. 启动后端服务器

```bash
uvicorn main:app --reload --port=11021
```

这将会在 `http://127.0.0.1:11021` 启动你的 FastAPI 应用。

## 总结

1. 克隆项目仓库。
2. 安装前端和后端依赖。
3. 修改后端数据库配置。
4. 导入数据库文件。
5. 启动前端和后端服务器。

现在，你应该可以通过 `http://localhost:5173` 访问你的前端应用，并通过 `http://127.0.0.1:11021` 访问你的后端 API。

如果有任何问题，请随时告诉我。