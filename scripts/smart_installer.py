#!/usr/bin/env python3
"""
智能Python环境检测和包安装脚本
自动检测当前环境并选择合适的离线安装包
"""

import os
import sys
import platform
import subprocess
import json
import glob
from pathlib import Path
import zipfile
import tarfile

class EnvironmentDetector:
    """环境检测器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.python_implementation = platform.python_implementation()
        
    def get_platform_tag(self):
        """获取平台标签"""
        if self.system == "windows":
            if self.machine in ["amd64", "x86_64"]:
                return "win_amd64"
            else:
                return "win32"
        elif self.system == "linux":
            if self.machine == "x86_64":
                return "linux_x86_64"
            elif self.machine.startswith("arm") or self.machine == "aarch64":
                return "linux_aarch64"
        elif self.system == "darwin":
            if self.machine == "x86_64":
                return "macosx_10_9_x86_64"
            elif self.machine == "arm64":
                return "macosx_11_0_arm64"
        return "unknown"
    
    def detect_virtual_env(self):
        """检测虚拟环境"""
        venv_info = {
            "in_venv": False,
            "venv_type": None,
            "venv_path": None
        }
        
        # 检测各种虚拟环境
        if hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        ):
            venv_info["in_venv"] = True
            
            if os.environ.get('CONDA_DEFAULT_ENV'):
                venv_info["venv_type"] = "conda"
                venv_info["venv_path"] = os.environ.get('CONDA_PREFIX')
            elif os.environ.get('VIRTUAL_ENV'):
                venv_info["venv_type"] = "virtualenv"
                venv_info["venv_path"] = os.environ.get('VIRTUAL_ENV')
            elif hasattr(sys, 'real_prefix'):
                venv_info["venv_type"] = "virtualenv"
                venv_info["venv_path"] = sys.prefix
            else:
                venv_info["venv_type"] = "venv"
                venv_info["venv_path"] = sys.prefix
        
        return venv_info
    
    def get_environment_info(self):
        """获取完整环境信息"""
        venv_info = self.detect_virtual_env()
        
        return {
            "system": self.system,
            "machine": self.machine,
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
            "python_executable": sys.executable,
            "platform_tag": self.get_platform_tag(),
            "virtual_env": venv_info,
            "pip_version": self.get_pip_version()
        }
    
    def get_pip_version(self):
        """获取pip版本"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split()[1]
        except:
            pass
        return "unknown"

class PackageInstaller:
    """包安装器"""
    
    def __init__(self, packages_dir="packages"):
        self.packages_dir = Path(packages_dir)
        self.detector = EnvironmentDetector()
        self.env_info = self.detector.get_environment_info()
        
    def find_matching_packages(self):
        """查找匹配当前环境的包目录"""
        platform_tag = self.env_info["platform_tag"]
        python_version = self.env_info["python_version"]
        
        # 可能的目录名模式
        patterns = [
            f"*{self.env_info['system']}*py{python_version.replace('.', '')}*",
            f"*{platform_tag}*",
            f"*python{python_version}*",
            f"*py{python_version.replace('.', '')}*"
        ]
        
        matching_dirs = []
        for pattern in patterns:
            matches = list(self.packages_dir.glob(pattern))
            matching_dirs.extend(matches)
        
        # 去重并按匹配度排序
        matching_dirs = list(set(matching_dirs))
        matching_dirs.sort(key=lambda x: self.calculate_match_score(x.name))
        
        return matching_dirs
    
    def calculate_match_score(self, dirname):
        """计算目录名与当前环境的匹配分数"""
        score = 0
        dirname_lower = dirname.lower()
        
        # 系统匹配
        if self.env_info["system"] in dirname_lower:
            score += 10
        
        # Python版本匹配
        py_version = self.env_info["python_version"].replace(".", "")
        if f"py{py_version}" in dirname_lower:
            score += 20
        
        # 平台匹配
        if self.env_info["platform_tag"] in dirname_lower:
            score += 15
        
        # 架构匹配  
        if self.env_info["machine"] in dirname_lower:
            score += 5
        
        return score
    
    def install_from_directory(self, package_dir, packages=None):
        """从指定目录安装包"""
        if not package_dir.exists():
            raise FileNotFoundError(f"包目录不存在: {package_dir}")
        
        # 查找wheel文件
        wheel_files = list(package_dir.glob("*.whl"))
        if not wheel_files:
            raise FileNotFoundError(f"在目录 {package_dir} 中没有找到wheel文件")
        
        print(f"从目录安装包: {package_dir}")
        print(f"找到 {len(wheel_files)} 个wheel文件")
        
        # 构建安装命令
        cmd = [sys.executable, "-m", "pip", "install", 
               "--no-index", "--find-links", str(package_dir)]
        
        if packages:
            cmd.extend(packages)
        else:
            # 尝试从requirements.txt安装
            requirements_file = package_dir / "requirements_locked.txt"
            if requirements_file.exists():
                cmd.extend(["-r", str(requirements_file)])
            else:
                # 安装所有找到的包
                package_names = set()
                for wheel in wheel_files:
                    # 从wheel文件名提取包名
                    name = wheel.name.split("-")[0]
                    package_names.add(name)
                cmd.extend(list(package_names))
        
        # 执行安装
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 安装成功!")
            print(result.stdout)
        else:
            print("✗ 安装失败!")
            print(result.stderr)
            return False
        
        return True
    
    def verify_installation(self, packages):
        """验证包是否正确安装"""
        print("\n验证安装...")
        failed_packages = []
        
        for package in packages:
            try:
                __import__(package)
                print(f"✓ {package}")
            except ImportError as e:
                print(f"✗ {package}: {e}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\n警告: 以下包验证失败: {', '.join(failed_packages)}")
            return False
        else:
            print("\n所有包验证成功!")
            return True
    
    def interactive_install(self):
        """交互式安装"""
        print("Python环境离线包安装器")
        print("=" * 50)
        
        # 显示环境信息
        print("当前环境信息:")
        for key, value in self.env_info.items():
            if key != "virtual_env":
                print(f"  {key}: {value}")
        
        venv = self.env_info["virtual_env"]
        print(f"  虚拟环境: {'是' if venv['in_venv'] else '否'}")
        if venv["in_venv"]:
            print(f"    类型: {venv['venv_type']}")
            print(f"    路径: {venv['venv_path']}")
        
        print()
        
        # 查找匹配的包目录
        matching_dirs = self.find_matching_packages()
        if not matching_dirs:
            print("错误: 没有找到匹配当前环境的离线包目录")
            print(f"请确保在 {self.packages_dir} 目录中有相应的包文件")
            return False
        
        print("找到以下匹配的包目录:")
        for i, dir_path in enumerate(matching_dirs[:5], 1):  # 最多显示5个
            print(f"  {i}. {dir_path.name}")
        
        # 让用户选择
        while True:
            try:
                choice = input(f"\n选择要使用的包目录 (1-{min(5, len(matching_dirs))}): ")
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < min(5, len(matching_dirs)):
                    selected_dir = matching_dirs[choice_idx]
                    break
                else:
                    print("无效选择，请重试")
            except (ValueError, KeyboardInterrupt):
                print("\n取消安装")
                return False
        
        # 询问要安装的包
        packages_input = input("\n输入要安装的包名 (用空格分隔，留空安装全部): ").strip()
        packages = packages_input.split() if packages_input else None
        
        # 确认安装
        print(f"\n将要从 {selected_dir.name} 安装包")
        if packages:
            print(f"指定包: {', '.join(packages)}")
        else:
            print("将安装所有可用包")
        
        confirm = input("确认安装? (y/N): ").lower()
        if confirm != 'y':
            print("取消安装")
            return False
        
        # 执行安装
        success = self.install_from_directory(selected_dir, packages)
        
        if success and packages:
            self.verify_installation(packages)
        
        return success

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Python环境离线包安装器")
    parser.add_argument("--packages-dir", default="packages", 
                       help="离线包目录")
    parser.add_argument("--packages", nargs="*", 
                       help="要安装的包列表")
    parser.add_argument("--auto", action="store_true", 
                       help="自动选择最匹配的包目录")
    parser.add_argument("--info", action="store_true", 
                       help="只显示环境信息")
    
    args = parser.parse_args()
    
    installer = PackageInstaller(args.packages_dir)
    
    if args.info:
        print("环境信息:")
        print(json.dumps(installer.env_info, indent=2, ensure_ascii=False))
        return
    
    if args.auto:
        matching_dirs = installer.find_matching_packages()
        if matching_dirs:
            installer.install_from_directory(matching_dirs[0], args.packages)
        else:
            print("没有找到匹配的包目录")
    else:
        installer.interactive_install()

if __name__ == "__main__":
    main()