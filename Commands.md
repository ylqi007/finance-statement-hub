所有和 Python 相关的开发、安装、运行、测试，建议都在项目的 venv 中进行。


## 检查最常见的三个安装目录
### 1. 检查 Homebrew 安装的 Python 版本
```shell
$ ls -l /opt/homebrew/bin/python*
lrwxr-xr-x@ 1 ylqi007  admin  46 Jul 17 22:51 /opt/homebrew/bin/python3.13 -> ../Cellar/python@3.13/3.13.14_1/bin/python3.13
lrwxr-xr-x@ 1 ylqi007  admin  53 Jul 17 22:51 /opt/homebrew/bin/python3.13-config -> ../Cellar/python@3.13/3.13.14_1/bin/python3.13-config
```

### 2. 检查官网 .pkg 安装包的目录
```shell
$ ls -l /Library/Frameworks/Python.framework/Versions/
ls: /Library/Frameworks/Python.framework/Versions/: No such file or directory
```

### 3. 检查 Mac 系统自带的目录
```shell
$ type -a python3
python3 is /usr/bin/python3
```


## 使用 venv
### 创建
```shell
cd ~/Work/Finance/Finance-Statement-Hub

python3.13 --version
python3.13 -m venv .venv
```

### 激活 venv
```
source .venv/bin/activate
```


```shell
cd ~/Work/Finance/Finance-Statement-Hub

# 使用当前系统中选定的 Python 创建虚拟环境
python3 -m venv .venv

# 从这里开始进入虚拟环境
source .venv/bin/activate

# 升级虚拟环境自己的基础工具
python -m pip install --upgrade pip setuptools wheel

# 安装当前项目及开发依赖
python -m pip install -e ".[dev]"
```



安装项目
```shell
python -m pip install -e ".[dev]"
```

验证
```
python -m pip show finance-statement-hub
pytest --version
ruff --version
```