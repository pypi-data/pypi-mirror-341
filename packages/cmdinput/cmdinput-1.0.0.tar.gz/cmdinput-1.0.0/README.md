# 🚀 CMD-Input —— 让Python输入不再烫手！

![test](https://img.shields.io/badge/单元测试-100%25通过-brightgreen) 
![version](https://img.shields.io/badge/版本-1.0.0-ff69b4)

还在用 `input()` 玩字符串拼图？ 
🔥 **是时候升级你的输入方式了！** 🔥

```python
# 传统艺能 vs 现代魔法 ✨
a, b, c = map(int, input().split())  # ← 老古董写法
a, b, c = cmdinput.read(int, int, int)  # ← 优雅永不过时
```

## 🛠️ 快速上手
```bash
pip install cmdinput
```

```python
import cmdinput as cin

# 基本操作
name = cin.read(str)  # "请输入你的名字："

# 列表
matrix = cin.read([[float]*5]*6)  # 直接读取二维浮点数组

# 布尔值 🔮
is_admin, has_permission = cin.read(bool, bool)  # 自动识别True/False

# 自定义分隔符 🔧
data = cin.read(int, float, str, sep="|")  # 支持任意分隔符

# 类型转换 🔮
binary_num = cin.read(lambda x: int(x, 2))  # 自动转换二进制字符串

# 文件读取 📂
with open('data.txt') as f:
    x, y = cin.read(float, float, file=f)

```
## 📜 更新日志
- 2025.10.01: 1.0.0 发布  
  全新登场！输入从未如此优雅

---

> 👩💻 开发者友好 | 🐍 Pythonic设计 | 🚴 极简接入
