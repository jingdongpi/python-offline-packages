# 灵活构建指南

## 📋 概述

现在你可以在运行 GitHub Actions 时灵活选择要构建的平台和配置，无需修改代码！

**✨ 新功能**: 构建的离线包现在包含 pip 安装器，即使用户电脑没有安装 pip 也能正常使用！

## 🖥️ 系统要求

### 对于构建者（你）
- GitHub 账户和仓库
- 无需其他要求，GitHub Actions 会处理一切

### 对于最终用户
- **Python**: 对应版本的 Python 解释器（如 3.8.10、3.9.x 等）
- **pip**: 如果没有安装，构建的包会自动包含 pip 安装器
- **系统依赖**: 某些包可能需要系统级库（详见故障排除）

### 版本兼容性
- **Python 3.8.18** (构建) ↔ **Python 3.8.10** (用户) ✅ **兼容**
- **Python 3.9.x** (构建) ↔ **Python 3.9.y** (用户) ✅ **兼容**
- **Python 3.8.x** (构建) ↔ **Python 3.9.x** (用户) ❌ **不兼容**

## 🚀 使用方法

### 1. 手动触发构建

1. 访问你的 GitHub 仓库
2. 点击 **Actions** 标签页
3. 选择 **Build Python Packages for Multiple Environments** 工作流
4. 点击 **Run workflow** 按钮
5. 在弹出的表单中配置你的构建选项：

### 2. 构建选项说明

| 选项 | 描述 | 默认值 | 示例 |
|------|------|--------|------|
| **要下载的包列表** | 用空格分隔的包名 | `numpy scipy pandas matplotlib` | `tensorflow torch scikit-learn` |
| **是否使用自定义requirements.txt** | 使用项目中的 requirements.txt | `false` | 勾选以使用项目文件 |
| **构建 Windows 包** | 是否构建 Windows x86_64 | `true` | 取消勾选以跳过 Windows |
| **构建 Linux x86_64 包** | 是否构建 Linux x86_64 | `true` | 取消勾选以跳过 Linux x64 |
| **构建 Linux ARM64 包** | 是否构建 Linux ARM64 | `true` | 取消勾选以跳过 Linux ARM64 |
| **Python 版本** | 用逗号分隔的版本号 | `3.8,3.9,3.10,3.11,3.12` | `3.9,3.11` 或 `3.10` |

### 3. 常用构建场景

#### 场景1: 只构建 Linux ARM64
```
✅ 构建 Linux ARM64 包: true
❌ 构建 Windows 包: false  
❌ 构建 Linux x86_64 包: false
Python 版本: 3.9,3.10,3.11
```

#### 场景2: 只构建特定 Python 版本
```
✅ 构建 Windows 包: true
✅ 构建 Linux x86_64 包: true  
✅ 构建 Linux ARM64 包: true
Python 版本: 3.11
```

#### 场景3: 只构建机器学习包
```
包列表: torch tensorflow scikit-learn numpy pandas
Python 版本: 3.9,3.10,3.11
其他选项保持默认
```

## 🔄 构建触发方式

**只支持手动触发** - 为了更好的资源控制，现在只支持手动触发构建，不会在代码推送时自动构建。

要开始构建：
1. 访问 GitHub 仓库的 Actions 页面
2. 选择工作流并点击 "Run workflow"
3. 配置你的构建选项

## 📦 下载构建结果

构建完成后，可以在 Actions 页面的 **Artifacts** 部分下载对应平台的包：

- `packages-windows-x86_64-py39` - Windows Python 3.9 包
- `packages-linux-x86_64-py310` - Linux x64 Python 3.10 包  
- `packages-linux-aarch64-py311` - Linux ARM64 Python 3.11 包

## 🎯 最佳实践

1. **测试阶段**: 只选择一个平台和一个 Python 版本进行快速测试
2. **生产发布**: 选择全部平台和需要的 Python 版本
3. **特定需求**: 根据目标环境选择对应的平台组合

## ⚠️ 注意事项

- ARM64 构建可能需要更长时间
- 选择的 Python 版本越多，构建时间越长
- 确保包名拼写正确，错误的包名会导致构建失败
- 构建包会自动包含 pip 安装器，适用于没有 pip 的环境

## 🆘 故障排除

### 构建问题
如果构建失败：
1. 检查包名是否正确
2. 验证 Python 版本格式 (如: `3.9,3.10`)
3. 查看构建日志了解具体错误
4. 尝试减少包数量或 Python 版本进行测试

### 用户安装问题

#### 问题1: 用户没有 pip
**现象**: 运行 `pip` 命令提示 "command not found"
**解决**: 
- ✅ **自动处理**: 安装脚本会自动检测并安装 pip
- 🔧 **手动处理**: 运行 `python pip_installer/get-pip.py`

#### 问题2: Python 版本不匹配
**现象**: 提示版本不兼容
**解决**: 
- 同主次版本号兼容 (如 3.8.10 ↔ 3.8.18)
- 不同主次版本需重新构建

#### 问题3: 权限不足
**现象**: 安装时提示权限错误
**解决**:
- Linux/Mac: 使用 `--user` 参数
- Windows: 以管理员身份运行
