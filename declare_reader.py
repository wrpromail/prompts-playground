import yaml
import jinja2
from jinja2 import Environment, FileSystemLoader

def load_template_config(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def render_template_using_config(template_name, user_input, config):
    # 加载模板文件夹
    template_folder = config['template_folder']
    env = Environment(loader=FileSystemLoader(template_folder))
    
    # 寻找对应的模板配置
    template_config = next((item for item in config['template_declares'] if item['template_name'] == template_name), None)
    if not template_config:
        raise ValueError("Template name not found in configuration.")
    
    # 检查必须的字段是否存在
    required_keys = [key['name'] for key in template_config['key'] if key['required']]
    missing_keys = [key for key in required_keys if key not in user_input]
    if missing_keys:
        raise ValueError(f"Missing required fields: {', '.join(missing_keys)}")
    
    # 渲染模板
    template = env.get_template(template_config['template_path'])
    return template.render(user_input)

def render_template(template_declare: str, template_name: str, user_input: dict) -> str:
    config = load_template_config(template_declare)
    try:
        return render_template_using_config(template_name, user_input, config)
    except Exception as e:
        return f"Error: {str(e)}"
