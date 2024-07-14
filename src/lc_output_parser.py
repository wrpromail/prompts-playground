from pydantic import BaseModel, Field
from typing import Dict, Type, Any, Tuple
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.json import SimpleJsonOutputParser
from enum import Enum
from langchain.output_parsers.enum import EnumOutputParser
from langchain_core.output_parsers import JsonOutputParser

class SlideDeck(BaseModel):
    title: str = Field(description="幻灯片的标题")
    outline: list[str] = Field(description="幻灯片的大纲内容")


def get_pydantic_output_parser_ins():
    parser = PydanticOutputParser(pydantic_object=SlideDeck)
    format_instructions = parser.get_format_instructions()
    return format_instructions

def get_simple_json_output_parser_ins():
    parser = SimpleJsonOutputParser()
    format_instructions = parser.get_format_instructions()
    return format_instructions

def create_enum(name, entries):
    """ 动态创建枚举类
    :param name: 枚举类的名称
    :param entries: 字典，其中包含枚举的成员名称及其值
    :return: 枚举类
    """
    # Enum 的构造函数接受名称和成员列表
    return Enum(value=name, names=entries)

def get_enum_output_parser_ins(user_enum: dict):
    UserEnum = create_enum("userEnum", user_enum)
    parser = EnumOutputParser(enum=UserEnum)
    return parser.get_format_instructions()

def create_pydantic_model(name: str, fields: Dict[str, Tuple[type, Any, str]]) -> Type[BaseModel]:
    """
    动态创建 Pydantic 模型
    :param name: 模型的名称
    :param fields: 一个字典，键为字段名，值为 (字段类型, 默认值, 描述) 的元组
    :return: Pydantic 模型类
    """
    attributes = {field_name: (field_type, Field(default=default, description=desc))
                  for field_name, (field_type, default, desc) in fields.items()}
    # 应用类型注解到动态创建的模型类中
    new_model = type(name, (BaseModel,), {})
    for attr_name, (attr_type, field) in attributes.items():
        setattr(new_model, attr_name, field)
        new_model.__annotations__[attr_name] = attr_type
    return new_model

# 定义用户字段
user_fields = {
    "setup": (str, "", "Question to set up a joke"),
    "punchline": (str, "", "Answer to resolve the joke")
}

class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

# 创建模型
jokex = create_pydantic_model("Joke", user_fields)
    
# 创建 JsonOutputParser
#parser = JsonOutputParser(pydantic_object=jokex)
parser = JsonOutputParser(pydantic_object=Joke)
print(parser.get_format_instructions())