### 管理系统脚手架
用于快速开发定制业务系统 

### 虚拟环境配置
```
#建立虚拟环境
python3 -m venv venv
#激活虚拟环境
source venv/bin/activate
#安装项目依赖
pip install --upgrade pip  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
pip install -r requirements.txt  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
#运行程序
python app/main.py

#退出虚拟环境
deactivate

```

### 代码语法检查要求

```
1 新建 .git/hooks/pre-commit, 内容如下:

#!/usr/bin/env bash
flake8 ./app --ignore=F811, E501, W292, E999, E712

然后执行:
chmod +x .git/hooks/pre-commit

```

#### 核心功能
* 环境变量及配置管理
    * 全局配置文件
    * 环境变量文件加载
* 标准日志输出
    * Debug 模式下输出为控制台
    * 非Debug 模式下输出为文件及控制台
    * 日志文件可以自动按日志大小切分
* 数据库连接管理
    * 提供postgresql 服务
    * 提供数据库表自动创建功能 
    * 提供数据库表多版本Migrate功能
    * 提供非阻塞 ORM 功能
* 提供统一异常处理功能 
* 提供JWT Auth安全验证功能





#### 文件目录 
```
backend
-- main.py
-- core
---- __init__.py
---- config.py
---- logger.py
---- db.py
---- auth.py
-- logic 
---- common
------ __init__.py
------ user.py
---- usergroup.py
-- api 
---- __init__.py
-- tests
---- __init__.py
---- core
------ test_config.py
------ test_logger.py
------ test_db.py
------ test_auth.py
```
