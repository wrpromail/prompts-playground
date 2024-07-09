import os
import json

from texts import *
from src.llm_source import PublicGlm, LocalOllamaGlm
from declare_reader import render_template, load_template_config

import gradio as gr 

global ModelSource
global TemplateDeclareFile


def load_public_model(model_name: str, api_key: str):
    global ModelSource
    msg = "模型加载成功"
    if api_key and len(api_key) > 0:
        os.environ.setdefault('GLM_API_KEY', api_key)
    ModelSource = PublicGlm(model_name=model_name)
    try:
        ModelSource.init_llm()
    except Exception as e:
        msg = f"模型加载失败, {e}"
    return msg

def load_ollama_model(model_name: str, generate_url: str):
    global ModelSource
    msg = "模型加载成功"
    ModelSource = LocalOllamaGlm(generate_url, model_name)
    try:
        ModelSource.init_llm()
    except Exception as e:
        msg = f"模型加载失败, {e}"
    return msg

def load_transformers_model(model_path: str, tokenizer_path: str):
    pass


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
    

custom_infer_parameters_default = """
{
 "max_tokens":512,
 "infer_temperature":0.95, 
 "top_p":0.7,
 "do_sample": True,
}
"""

if __name__ == "__main__":
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    public_model_name = gr.Textbox(label="public_model_name", value="glm-4-air", lines=1, scale=2)
                    public_model_api_key = gr.Textbox(label="public_model_api_key", value="", lines=1, scale=2)
                    public_model_load_button = gr.Button("加载开放平台模型", scale=2)
                with gr.Row():
                    tgi_model_name = gr.Textbox(label="tgi_model_name", value="tgi", lines=1, scale=2)
                    tgi_generate_url = gr.Textbox(label="tgi_generate_url", value="", lines=1, scale=2)
                    tgi_model_load_button = gr.Button("加载tgi模型", scale=2)

                with gr.Row():
                    ollama_model_name = gr.Textbox(label="ollama_model_name", value="glm4", lines=1, scale=2)
                    ollama_generate_url = gr.Textbox(label="ollama_generate_url", value="http://127.0.0.1:11434/api/generate", lines=1, scale=2)
                    ollama_model_load_button = gr.Button("加载ollama模型", scale=2)

                with gr.Row():
                    transformers_model_path = gr.Textbox(label="transformers_model_path", value="", lines=1,scale=2)
                    transformers_tokenizer_path = gr.Textbox(label="transformers_tokenizer_path", value="", lines=1, scale=2)
                    transformers_model_load_button = gr.Button("加载transformers模型", scale=2)
                
                with gr.Row():
                    vllm_model_path = gr.Textbox(label="vllm_model_path", value="", lines=1, scale=2)
                    vllm_tokenizer_path = gr.Textbox(label="vllm_tokenizer_path", value="", lines=1, scale=2)
                    vllm_model_load_button = gr.Button("加载vllm模型", scale=2)    
                
                load_model_result = gr.Textbox(label="load_model_result", lines=1, scale=2)                
                
            with gr.Column(scale=5):
                with gr.Tab("使用说明"):
                    gr.Markdown(basic_usage_md)

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
                    custom_infer_parameters = gr.Textbox(label="custom_infer_parameters", lines=3, value=custom_infer_parameters_default)
                    infer_parameters_save = gr.Button("保存推理参数")

                    
        public_model_load_button.click(load_public_model, inputs=[public_model_name, public_model_api_key],outputs=[load_model_result])
        ollama_model_load_button.click(load_ollama_model, inputs=[ollama_model_name, ollama_generate_url], outputs=[load_model_result])
        transformers_model_load_button.click(load_transformers_model, inputs=[transformers_model_path, transformers_tokenizer_path], outputs=[load_model_result])

        generated_prompt_render_click.click(render_template_content, inputs=[template_name, user_parameters], outputs=[generated_prompt])
        generated_prompt_infer_click.click(template_infer, inputs=[generated_prompt], outputs=[generated_prompt_infer_text, generated_prompt_infer_usage ])
        prompt_declare_file_load.click(load_template_names,inputs=[prompt_declare_file], outputs=[template_load_message])
        # check_template_content.click 根据 template_name 读取模板路径，然后读取模板内容
        # generate_mock_user_parameters.click
    
    demo.launch(server_name="0.0.0.0")

