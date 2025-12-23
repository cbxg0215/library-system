# 图书馆管理系统（Library Management System）

## 一、项目简介
本项目是一个面向高校/社区图书馆的轻量级 Web 管理系统，采用 B/S 架构实现。  
系统实现了图书信息管理、用户登录、图书借阅与归还等核心功能，适合作为课程设计或实验项目使用。

## 二、技术栈
- 后端：Python + Flask  
- 前端：HTML + CSS  
- 数据库：SQLite  
- 运行环境：本地 Web 服务

## 三、项目结构
library-system/
│
├── app.py # Flask 主程序（路由与业务逻辑）
├── db.py # 数据库初始化脚本
├── library.db # SQLite 数据库文件（首次运行生成）
│
├── templates/ # 前端页面模板
│ ├── login.html
│ ├── books.html
│ └── borrow.html
│
├── static/ # 静态资源
│ └── style.css
│
├── test/ # 测试代码（示例）
│
└── README.md # 项目说明文档

shell
复制代码

## 四、运行环境要求
- Python 3.8 及以上版本  
- pip 包管理工具  

## 五、运行步骤

### 1. 安装依赖
```bash
pip install flask
或：

bash
复制代码
python -m pip install flask
2. 初始化数据库
在项目根目录执行：

bash
复制代码
python db.py
执行成功后会生成 library.db 数据库文件。

3. 启动系统
bash
复制代码
python app.py
启动成功后终端会显示：

nginx
复制代码
Running on http://127.0.0.1:5000
4. 访问系统
在浏览器中打开：

cpp
复制代码
http://127.0.0.1:5000
六、默认账号
系统内置管理员账号：

pgsql
复制代码
用户名：admin
密码：123456
七、主要功能
用户登录与会话管理

图书信息管理（入库、查询）

图书借阅与归还

借阅记录查询


八、说明
本项目为教学与课程设计用途，采用轻量级技术实现，未涉及复杂权限控制与安全加密机制。
如需扩展，可进一步引入前后端分离架构或更完善的数据库系统。

九、作者说明
本项目由课程设计完成，作为学习 Web 应用开发与软件工程流程的实践成果。
