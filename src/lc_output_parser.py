from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.json import SimpleJsonOutputParser

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

print(get_simple_json_output_parser_ins())
