# AI-Man: Linux命令智能助手

AI-Man (aiman) 是一个基于大语言模型的Linux命令智能提示工具，它能够帮助用户快速回忆和掌握Linux命令的用法。

## 功能特点

- **基础查询模式**
  - 快速获取命令的基本用法
  - 展示最常用的2-3个核心参数
  - 提供1-2个常见使用示例

- **详细查询模式**
  - 展示完整的命令说明
  - 列出5-8个重要参数及其用途
  - 提供3-4个不同场景的使用示例
  - 包含常用参数组合说明
  - 包含重要注意事项

## 系统要求

- Python 3.8+
- pip (Python包管理器)

## 安装方法

1. 克隆仓库
```bash
git clone https://github.com/Yong5520/aiman.git
cd aiman
```

2. 安装依赖
```bash
# 使用系统pip安装依赖
sudo pip3 install -r requirements.txt
```

3. 安装到系统
```bash
# 将脚本安装到系统目录
sudo cp aiman.py /usr/local/bin/aiman
sudo chmod +x /usr/local/bin/aiman

# 创建配置目录并复制配置文件
sudo mkdir -p /etc/aiman
sudo cp config.yaml /etc/aiman/
sudo chmod 644 /etc/aiman/config.yaml

# 可选：创建用户级配置目录
mkdir -p ~/.config/aiman
cp config.yaml ~/.config/aiman/  # 用户可以在这里覆盖系统配置
```

4. 配置LLM服务
```bash
aiman --config
```

## 使用方法

1. 基础查询 - 获取命令的基本用法：
```bash
aiman ls
```

2. 详细查询 - 获取命令的完整说明：
```bash
aiman ls -d
```

3. 配置LLM - 更新LLM服务配置：
```bash
aiman --config
```

## 配置说明

### LLM配置
通过 `aiman --config` 进行交互式配置：
- Base URL: LLM服务的API地址
- API Key: 访问密钥
- Model: 使用的模型名称

### 配置文件
配置文件位于 `/etc/aiman/config.yaml`，包含：
```yaml
api:
  base_url: https://api.deepseek.com （强烈推荐使用deepseek, 其他模型请自行配置）
  key: your-api-key
  model: model-name
```

## 项目结构
```
/usr/local/bin/aiman     # 主程序
/etc/aiman/config.yaml   # 配置文件
```

## 依赖要求

- Python 3.8+
- openai>=1.0.0
- pyyaml>=5.1
- requests>=2.25.1

## 常见问题

1. **配置问题**
   - 确保已正确配置LLM服务
   - 检查API Key是否有效
   - 确认网络连接正常

2. **使用问题**
   - 命令查询区分大小写
   - 支持管道符号等特殊字符

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目：
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 作者

[曹永](https://github.com/Yong5520)

## 致谢

- 所有贡献者