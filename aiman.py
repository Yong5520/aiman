#!/usr/bin/python3

import sys
import yaml
import argparse
from openai import OpenAI
import os

class AiMan:
    def __init__(self):
        self.config = self._load_config()
        self.client = None  # 初始化时不创建client
        
    def _load_config(self):
        # 配置文件的可能位置
        config_paths = [
            '/etc/aiman/config.yaml',                    # 系统级配置
            os.path.expanduser('~/.config/aiman/config.yaml')  # 用户级配置
        ]
        
        config = {}  # 初始化空配置
        config_found = False
        
        # 按顺序加载配置文件，后加载的会覆盖先加载的
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        current_config = yaml.safe_load(f)
                        if current_config:  # 确保加载的配置不是None
                            config_found = True
                            # 递归合并配置
                            config = self._merge_configs(config, current_config)
                except Exception as e:
                    print(f"Error reading config file {config_path}: {e}")
                    continue
        
        if not config_found:
            # 如果没有找到任何配置文件
            raise FileNotFoundError("No config file found. Please run 'aiman --config' to set up configuration.")
        
        return config

    def _merge_configs(self, base, override):
        """递归合并配置字典"""
        merged = base.copy()
        
        for key, value in override.items():
            # 如果两个值都是字典，递归合并
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # 否则直接覆盖
                merged[key] = value
            
        return merged

    def _save_config(self, new_config):
        """保存配置到用户目录"""
        user_config_dir = os.path.expanduser('~/.config/aiman')
        user_config_path = os.path.join(user_config_dir, 'config.yaml')
        
        try:
            # 确保配置目录存在
            os.makedirs(user_config_dir, exist_ok=True)
            
            # 如果用户配置文件不存在，先从系统配置复制基础内容
            if not os.path.exists(user_config_path):
                system_config_path = '/etc/aiman/config.yaml'
                if os.path.exists(system_config_path):
                    with open(system_config_path, 'r', encoding='utf-8') as f:
                        base_config = yaml.safe_load(f)
                    # 更新基础配置中的 API 相关设置
                    base_config.update(new_config)
                    new_config = base_config
            
            # 保存配置文件
            with open(user_config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(new_config, f, allow_unicode=True)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def _init_client(self, api_config):
        """使用给定配置初始化客户端"""
        return OpenAI(
            api_key=api_config['key'],
            base_url=api_config['base_url']
        )

    def _get_non_empty_input(self, prompt):
        """获取非空用户输入"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("输入不能为空，请重新输入")

    def test_connection(self, api_config):
        """测试LLM连接"""
        try:
            client = self._init_client(api_config)
            response = client.chat.completions.create(
                model=api_config['model'],
                messages=[
                    {"role": "user", "content": "test connection"}
                ],
                stream=False
            )
            return True
        except Exception as e:
            print(f"连接测试失败: {str(e)}")
            return False

    def configure_llm(self):
        """配置LLM连接信息"""
        print("请配置LLM连接信息：\n")
        
        # 获取用户输入
        base_url = self._get_non_empty_input("Base URL: ")
        key = self._get_non_empty_input("API Key: ")
        model = self._get_non_empty_input("Model: ")

        # 创建新配置
        new_config = self.config.copy()
        new_config['api'] = {
            'base_url': base_url,
            'key': key,
            'model': model
        }

        # 测试连接
        print("\n正在测试连接...")
        if self.test_connection(new_config['api']):
            print("连接测试成功！")
            if self._save_config(new_config):
                print("配置已保存到config.yaml")
                return True
            else:
                print("配置保存失败")
                return False
        else:
            print("配置未保存")
            return False

    def get_command_help(self, command, detail=False):
        # 确保client已初始化
        if not self.client:
            self.client = self._init_client(self.config['api'])
            
        try:
            # 根据detail参数选择提示词模板
            template_key = 'command_detail' if detail else 'command_basic'
            
            # 检查模板是否存在
            if template_key not in self.config['prompts']:
                raise KeyError(f"Template '{template_key}' not found in config")
                
            prompt = self.config['prompts'][template_key].format(command=command)
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.config['api']['model'],
                messages=[
                    {"role": "system", "content": "You are a Linux command expert."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            
            # 返回结果
            return response.choices[0].message.content
        except KeyError as e:
            return f"Configuration error: {str(e)}"
        except Exception as e:
            return f"API error: {str(e)}\nPlease check your API configuration and internet connection."

def main():
    parser = argparse.ArgumentParser(description='Linux command AI assistant')
    parser.add_argument('command', nargs='?', help='The command to query')
    parser.add_argument('-d', '--detail', action='store_true', help='Show detailed help')
    parser.add_argument('--config', action='store_true', help='Configure LLM settings')
    
    args = parser.parse_args()
    
    aiman = AiMan()

    if args.config:
        aiman.configure_llm()
        return

    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    result = aiman.get_command_help(args.command, detail=args.detail)
    print(result)

if __name__ == "__main__":
    main() 