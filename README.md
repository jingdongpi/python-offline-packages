# Python离线包构建和安装工具

这个项目提供了一个完整的解决方案，用于构建和分发Python包的离线安装包，支持多种操作系统、Python版本和架构。

## 🚀 特性

- ✅ **多环境支持**: Windows x86-64、Linux x86-64、Linux ARM64
- ✅ **多Python版本**: 3.8、3.9、3.10、3.11、3.12
- ✅ **精准架构支持**: 针对性优化的三个主流平台
- ✅ **自动化构建**: GitHub Actions自动构建
- ✅ **智能安装**: 自动检测环境并选择合适的包
- ✅ **场景预设**: 科学计算、机器学习、数据分析等

## 🎯 支持的平台

| 平台 | 架构 | Python版本 | 状态 |
|------|------|------------|------|
| Windows | x86-64 | 3.8 - 3.12 | ✅ 完全支持 |
| Linux | x86-64 | 3.8 - 3.12 | ✅ 完全支持 |
| Linux | ARM64 | 3.8 - 3.12 | ✅ 预编译包支持 |

## 📁 项目结构

```
python-offline-packages/
├── .github/workflows/build-packages.yml    # GitHub Actions构建配置
├── config/build-config.yml                 # 构建配置文件
├── scripts/smart_installer.py              # 智能安装脚本
├── requirements/                            # 不同场景的需求文件
├── packages/                                # 构建产物目录
└── docs/                                    # 文档
```

## 🛠️ 使用方法

### 对于开发者（构建离线包）

1. **Fork这个仓库**
2. **修改配置文件**:
   - 编辑 `config/build-config.yml` 定义支持的环境
   - 修改 `requirements/*.txt` 定义包需求
3. **推送代码触发构建**:
   ```bash
   git add .
   git commit -m "Update package requirements"
   git push origin main
   ```
4. **下载构建产物**: 在GitHub Actions页面下载各环境的离线包

### 对于最终用户（安装离线包）

#### 方法1: 智能安装（推荐）
```bash
# 下载并解压所有环境的包到packages目录
python scripts/smart_installer.py
```

#### 方法2: 手动选择环境
```bash
# 下载对应环境的包并解压
cd packages/packages-your-platform-pyXX-arch/
./install.sh  # Linux/Mac
# 或
install.bat   # Windows
```

#### 方法3: 直接使用pip
```bash
pip install --no-index --find-links ./packages-your-env numpy scipy pandas
```

## 📋 支持的包组合

| 场景 | 包含的主要包 | 适用人群 |
|------|-------------|----------|
| 科学计算 | numpy, scipy, matplotlib, sympy | 科研人员、工程师 |
| 机器学习 | scikit-learn, pandas, seaborn, xgboost | 数据科学家 |
| 数据分析 | pandas, plotly, jupyter, openpyxl | 业务分析师 |
| 深度学习 | tensorflow, pytorch, opencv | AI工程师 |

## 🏗️ 构建详情

### 支持的架构
- **Windows x86-64**: 使用 `windows-latest` runner，完整支持所有Python版本
- **Linux x86-64**: 使用 `ubuntu-latest` runner，原生支持
- **Linux ARM64**: 使用预编译包下载技术，支持所有Python版本

### 构建产物
每个平台/Python版本组合都会生成独立的构建产物：
- `packages-windows-latest-pyXX-x64/` - Windows x86-64包
- `packages-ubuntu-latest-pyXX-x64/` - Linux x86-64包
- `packages-ubuntu-latest-pyXX-aarch64/` - Linux ARM64包

## 📖 详细文档

- [安装指南](docs/installation-guide.md)
- [故障排除](docs/troubleshooting.md)
- [自定义构建](docs/custom-build.md)
- [ARM64支持说明](docs/arm64-support.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！特别欢迎：
- 新包配置的贡献
- ARM64兼容性测试反馈
- 文档改进建议

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情