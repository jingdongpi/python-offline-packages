# 故障排除指南

## 常见问题及解决方案

### ❌ 问题1: pip未安装或不可用

**错误信息**:
```
❌ 错误: pip未安装或不可用
'pip' 不是内部或外部命令，也不是可运行的程序
```

**解决方案**:

#### 方法1: 使用get-pip.py (推荐)
离线包中包含了 `get-pip.py` 文件：
```bash
# 检查文件是否存在
ls get-pip.py

# 安装pip
python get-pip.py

# 验证安装
python -m pip --version
```

#### 方法2: 系统包管理器

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

**CentOS/RHEL**:
```bash
sudo yum install python3-pip
# 或者 (较新版本)
sudo dnf install python3-pip
```

**Fedora**:
```bash
sudo dnf install python3-pip
```

#### 方法3: Windows重新安装Python
1. 从 [python.org](https://www.python.org/downloads/windows/) 下载Python
2. 安装时**务必勾选** "Add pip to PATH"
3. 重新安装后验证: `python -m pip --version`

### ❌ 问题2: Python版本不匹配

**错误信息**:
```
⚠️ 警告: Python版本不匹配！
当前版本: 3.8.10
包版本: 3.8.18
```

**解决方案**:
- **3.8.x 系列互相兼容** - 可以继续安装
- **3.8 vs 3.9** - 不兼容，需要下载对应版本的包
- 建议选择 "y" 继续安装，通常可以正常工作

### ❌ 问题3: 权限错误

**错误信息**:
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**解决方案**:

#### Linux/Mac:
```bash
# 方法1: 用户级安装 (推荐)
python -m pip install --user --no-index --find-links . -r requirements_locked.txt

# 方法2: 使用虚拟环境
python -m venv myenv
source myenv/bin/activate
./install.sh

# 方法3: 使用sudo (不推荐)
sudo ./install.sh
```

#### Windows:
```cmd
# 以管理员身份运行命令提示符或PowerShell
# 右键点击 "以管理员身份运行"
install.bat
```

### ❌ 问题4: 网络错误 (构建时)

**错误信息**:
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**:
1. **检查包名拼写**是否正确
2. **检查网络连接**
3. **使用国内镜像** (中国用户):
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
```

### ❌ 问题5: 系统级依赖缺失

**错误信息**:
```
Building wheel for package failed
```

**解决方案**:

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev
# 对于特定包
sudo apt-get install libffi-dev libssl-dev
```

#### CentOS/RHEL:
```bash
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel libffi-devel openssl-devel
```

#### Windows:
- 安装 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- 或安装 Visual Studio Community

### ❌ 问题6: 虚拟环境问题

**创建和使用虚拟环境**:
```bash
# 创建虚拟环境
python -m venv offline_env

# 激活 (Linux/Mac)
source offline_env/bin/activate

# 激活 (Windows)
offline_env\Scripts\activate

# 在虚拟环境中安装
./install.sh

# 退出虚拟环境
deactivate
```

### ❌ 问题7: 架构不匹配

**错误信息**:
```
ERROR: package-1.0.0-cp39-cp39-linux_x86_64.whl is not a supported wheel on this platform
```

**解决方案**:
1. **确认架构**: `uname -m` (Linux) 或 `echo $PROCESSOR_ARCHITECTURE` (Windows)
2. **下载正确的包**: 选择匹配的 ARM64/x86_64 版本
3. **强制安装** (谨慎使用):
```bash
pip install package.whl --force-reinstall --no-deps
```

## 🔍 诊断命令

运行这些命令来诊断问题：

```bash
# 检查Python信息
python --version
python -c "import platform; print(f'Architecture: {platform.machine()}')"
python -c "import sys; print(f'Platform: {sys.platform}')"

# 检查pip信息  
python -m pip --version
python -m pip list

# 检查环境
echo $PATH  # Linux/Mac
echo %PATH% # Windows

# 检查已安装的包
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
```

## 🆘 获取帮助

如果以上方案都无法解决问题：

1. **收集信息**:
   - Python版本: `python --version`
   - 操作系统: `uname -a` 或系统信息
   - 完整错误信息
   - 使用的安装包名称

2. **检查日志**: 查看完整的错误输出

3. **尝试最小化安装**:
```bash
# 只安装一个包进行测试
python -m pip install --no-index --find-links . numpy
```

4. **社区支持**: 
   - Python官方文档
   - Stack Overflow
   - 相关包的GitHub Issues
