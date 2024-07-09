import os
import json

from texts import *
from src.llm_source import PublicGlm
from declare_reader import render_template, load_template_config

import gradio as gr 

global ModelSource
global TemplateDeclareFile

def load_model_click(method: str, model_source: str, model_name: str):
    global ModelSource
    msg = "模型加载成功"
    if method == "public_api":
        if model_source and len(model_source) > 0:
            os.environ.setdefault('GLM_API_KEY', model_source)
        ModelSource = PublicGlm()
    try:
        ModelSource.init_llm()
    except Exception as e:
        msg = f"模型加载失败, {e}"
    return msg

def load_template_names(yaml_file: str) -> list:
    global TemplateDeclareFile
    try:
        config = load_template_config(yaml_file)
        rst = []
        for item in config["template_declares"]:
            td = {}
            tn = item.get("template_name", None)
            if tn:
                td["template_name"] = tn
                td["example_input"] = item.get("example_input", None)
                td["description"] = item.get("description", None)
                keys = item.get("key", [])
                required_keys = []
                optional_keys = []
                for key in keys:
                    if key.get("required", False):
                        required_keys.append(key.get("name"))
                    else:
                        optional_keys.append(key.get("name"))
                td["required_keys"] = required_keys
                td["optional_keys"] = optional_keys
                rst.append(td)
        TemplateDeclareFile = yaml_file
        return rst
    except Exception as e:
        return []
        
    
def render_template_content(template_name: str, user_parameters: str):
    global TemplateDeclareFile
    return render_template(TemplateDeclareFile, template_name, json.loads(user_parameters))

def template_infer(prompt: str):
    global ModelSource
    if ModelSource is None:
        return "请先加载模型"
    # 使用全局变量加载推理变量
    rst = ModelSource.infer(prompt)
    return rst['response'], rst['usage']
    

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown(introduce_md)
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(model_load_md)
                invoke_method = gr.Dropdown(["public_api", "local_transformer"], value="API调用", label="invoke_method", scale=1)
                model_source = gr.Textbox(label="model_source", value="api key或本地模型地址",lines=1, scale=1)
                model_name = gr.Textbox(label="model_name", value="", lines=1, scale=1)
                max_tokens = gr.Number(label="infer_max_tokens", value=512, step=1, minimum=1, maximum=8192, scale=1)
                temperature = gr.Number(label="infer_temperature", value=0.95, step=0.01, minimum=0, maximum=1, scale=1)
                top_p = gr.Number(label="infer_top_p", value=0.70, step=0.01, minimum=0, maximum=1, scale=1)
                load_model = gr.Button(value="加载模型")
                load_model_result = gr.Textbox(label="load_model_result", lines=1)
            with gr.Column(scale=4):
                with gr.Tab("模板数据读取"):
                    prompt_declare_file = gr.Textbox(label="prompt_declare_file", value="prompt_declare.yml", scale=1)
                    prompt_declare_file_load = gr.Button(value="加载模板配置")
                    template_load_message = gr.JSON(label="template_load_message", scale=1)
                with gr.Tab("单个模板渲染与推理"):
                    template_name = gr.Textbox(label="template_name", scale=1)
                    with gr.Row():
                        check_template_content = gr.Button(value="查看模板内容")
                        generate_mock_user_parameters = gr.Button(value="生成模拟用户输入参数")
                    user_parameters = gr.Code(label="user_parameters", value='{}', language="json")
                    generated_prompt = gr.Textbox(label="generated_prompt", lines=3, show_copy_button=True)
                    with gr.Row():
                        generated_prompt_render_click = gr.Button(value="渲染 prompt")
                        generated_prompt_infer_click = gr.Button(value="推理 prompt")
                    with gr.Row():
                        generated_prompt_infer_text = gr.Textbox(label="generated_prompt_infer",scale=3)
                        generated_prompt_infer_usage = gr.JSON(label="generated_prompt_infer_usage", scale=1)

                    
        load_model.click(load_model_click, inputs=[invoke_method, model_source, model_name],outputs=[load_model_result])
        generated_prompt_render_click.click(render_template_content, inputs=[template_name, user_parameters], outputs=[generated_prompt])
        generated_prompt_infer_click.click(template_infer, inputs=[generated_prompt], outputs=[generated_prompt_infer_text, generated_prompt_infer_usage ])
        prompt_declare_file_load.click(load_template_names,inputs=[prompt_declare_file], outputs=[template_load_message])
        # check_template_content.click 根据 template_name 读取模板路径，然后读取模板内容
        # generate_mock_user_parameters.click
    
    demo.launch(server_name="0.0.0.0")

