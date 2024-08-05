from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class SlideContent(BaseModel):
    SlidePageTitle: str = Field(description="单页幻灯片的标题")
    SlidePageOutline: List = Field(description="单页幻灯片的大纲列表")


class SlideContentList(BaseModel):
    pairs: List[SlideContent]

parser = JsonOutputParser(pydantic_object=SlideContentList)
print(parser.get_format_instructions())

# 通过 JsonOutputParser 
