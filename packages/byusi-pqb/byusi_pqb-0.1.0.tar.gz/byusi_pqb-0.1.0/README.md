# pqb - Python Quick Bridge

[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://gitee.com/byusi/pqb/blob/main/LICENSE)
[![python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

**pqb** 是一个简化 Python 语法并兼容 Python 生态的轻量级编程语言，支持与原生 Python 代码无缝互操作。

项目地址：🖥️ [https://gitee.com/byusi/pqb](https://gitee.com/byusi/pqb)

## ✨ 特性亮点

- **简化语法**：使用 `t python:` 代码块原生嵌入 Python 代码
- **完全兼容**：支持导入和使用任意 Python 标准库及第三方库
- **开发友好**：
  - 内置基于 rich 库的彩色日志输出
  - 提供即时执行的命令行工具
  - 支持 .pqb 文件直接导入 Python 项目
- **零成本迁移**：自动转换 pqb 代码为 Python 代码
- **混合编程**：可在同一项目中自由组合 pqb 和 Python 文件

## 📦 安装方式

### 标准安装 (PyPI)
```bash
pip install pqb
```

### 从源码安装
```bash
pip install git+https://gitee.com/byusi/pqb.git
```

## 🚀 快速开始

### 示例代码 (`demo.pqb`)
```pqb
ib math

t python:
def calculate_sphere_volume(r):
    return 4/3 * math.pi * r**3
end python

print("Volume of sphere (r=3):", calculate_sphere_volume(3))
```

### 执行脚本
```bash
pqb demo.pqb
```

### 嵌入 Python 项目
```python
# main.py
import pqb  # 自动激活 pqb 导入器
import demo  # 导入 demo.pqb

print("Volume doubled:", demo.calculate_sphere_volume(5)*2)
```

## 📚 语法指南

### Python 代码块
```pqb
t python:
# 原生 Python 代码
from datetime import datetime
end python
```

### 模块导入
```pqb
ib requests         # 等效 import requests
ib pandas as pd    # 等效 import pandas as pd
```

### 混合编程
```pqb
ib numpy as np

t python:
def generate_matrix(size):
    return np.random.randn(size, size)
end python

print("3x3 matrix:\n", generate_matrix(3))
```

## 🛠️ 开发工具

### 代码转换
```bash
pqb input.pqb -o output.py
```

### 调试模式
```bash
pqb --debug demo.pqb
```

## 🤝 参与贡献

欢迎通过以下方式参与项目：
1. 提交 Issues 报告问题或建议
2. 发起 Pull Request 贡献代码
3. 完善文档或测试用例
4. 在社区分享使用案例

## 📜 开源协议

本项目采用 [MIT License](https://gitee.com/byusi/pqb/blob/main/LICENSE)，您可以自由地：
- 使用、复制和修改软件
- 进行商业性使用
- 无担保免责