# 离线包安装指南

## 系统要求

- Python 3.8+ 已安装
- pip 工具可用
- 足够的磁盘空间（通常需要500MB-2GB，取决于包的数量）

## 安装步骤

### 步骤1: 下载离线包

从GitHub Releases页面或Actions页面下载适合你系统的离线包。

**选择正确的包**:
- 文件名格式: `packages-{系统}-py{版本}-{架构}.zip`
- 例如: `packages-windows-latest-py311-x64.zip`

**系统对应关系**:
| 你的系统 | 选择文件名包含 |
|----------|----------------|
| Windows 64位 | `windows-latest-py*-x64` |
| Windows 32位 | `windows-latest-py*-x86` |
| Linux 64位 | `ubuntu-latest-py*-x64` |
| macOS Intel | `macos-latest-py*-x64` |
| macOS Apple Silicon | `macos-latest-py*-arm64` |

### 步骤2: 解压文件

```bash
# 创建工作目录
mkdir python-packages
cd python-packages

# 解压下载的文件
unzip packages-your-system-py311-x64.zip
```

### 步骤3: 选择安装方法

#### 方法A: 使用智能安装脚本（推荐）

```bash
# 如果下载了多个环境的包，使用智能脚本
python smart_installer.py

# 脚本会自动：
# 1. 检测你的Python环境
# 2. 找到最匹配的包目录
# 3. 引导你完成安装过程
```

#### 方法B: 使用预置安装脚本

```bash
# 进入对应的包目录
cd packages-windows-latest-py311-x64/

# Windows用户
install.bat

# Linux/Mac用户
chmod +x install.sh
./install.sh
```

#### 方法C: 手动pip安装

```bash
# 进入包目录
cd packages-windows-latest-py311-x64/

# 安装所有包
pip install --no-index --find-links . -r requirements_locked.txt

# 或安装特定包
pip install --no-index --find-links . numpy scipy pandas
```

### 步骤4: 验证安装

```python
# 运行Python并测试
python -c "
import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
print('所有包安装成功！')
print(f'NumPy版本: {np.__version__}')
print(f'SciPy版本: {scipy.__version__}')
print(f'Pandas版本: {pd.__version__}')
"
```

## 常见问题解决

### Q1: 提示"没有找到匹配的分发版本"
**原因**: Python版本不匹配
**解决**: 
1. 检查你的Python版本: `python --version`
2. 下载对应版本的离线包
3. 或使用包含依赖的版本: `pip install --no-index --find-links ./with_deps numpy`

### Q2: 安装过程中出现权限错误
**解决**: 
```bash
# 使用用户安装模式
pip install --user --no-index --find-links . numpy scipy

# 或使用虚拟环境
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# myenv\Scripts\activate.bat  # Windows
pip install --no-index --find-links . numpy scipy
```

### Q3: 某些包安装失败
**原因**: 缺少系统依赖或二进制不兼容
**解决**:
1. 尝试安装系统依赖（如Visual C++ Redistributable）
2. 使用conda环境: `conda install numpy scipy`
3. 从源码编译: `pip install --no-binary numpy scipy`

### Q4: 虚拟环境中安装
```bash
# 创建虚拟环境
python -m venv offline_env

# 激活环境
source offline_env/bin/activate  # Linux/Mac
offline_env\Scripts\activate.bat  # Windows

# 在虚拟环境中安装
pip install --no-index --find-links ./packages numpy scipy
```

## 高级用法

### 批量安装多个环境
```bash
# 为多个项目准备环境
for env in project1 project2 project3; do
    python -m venv $env
    source $env/bin/activate
    pip install --no-index --find-links ./packages -r requirements.txt
    deactivate
done
```

### 创建自己的离线包
```bash
# 下载当前环境的所有包
pip freeze > current_requirements.txt
pip download -r current_requirements.txt -d my_packages/

# 在其他机器上安装
pip install --no-index --find-links ./my_packages -r current_requirements.txt
```

## 性能优化建议

1. **使用SSD**: 离线包文件较多，SSD能显著提升安装速度
2. **关闭杀毒软件**: 临时关闭实时扫描可加速安装
3. **批量安装**: 一次性安装所有需要的包，避免多次调用pip
4. **清理缓存**: 安装完成后清理pip缓存释放空间

```bash
# 清理pip缓存
pip cache purge
```