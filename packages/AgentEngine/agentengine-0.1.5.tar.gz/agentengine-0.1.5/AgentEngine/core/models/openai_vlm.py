import base64
from typing import List, Optional, Dict, Any

from smolagents.models import ChatMessage
from AgentEngine.core.utils.observer import MessageObserver, ProcessType

from AgentEngine.core.models import OpenAIModel


class OpenAIVLModel(OpenAIModel):
    def __init__(
        self, 
        observer: MessageObserver, 
        temperature=0.7, 
        top_p=0.7, 
        frequency_penalty=0.5,
        max_tokens=512,
        *args, 
        **kwargs
    ):
        super().__init__(observer=observer, *args, **kwargs)
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self._current_request = None  # 用于存储当前请求


    def encode_image(self, image_path: str) -> str:
        """
        将图像文件编码为base64字符串
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            str: base64编码后的图像数据
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    def prepare_image_message(self, image_path: str, system_prompt: str = "Describe this picture.") -> List[Dict[str, Any]]:
        """
        准备包含图像的消息格式
        
        Args:
            image_path: 图像文件路径
            system_prompt: 系统提示词
            
        Returns:
            List[Dict[str, Any]]: 准备好的消息列表
        """
        base64_image = self.encode_image(image_path)
        
        messages = [
            {
                "role": "system",
                "content": [{"text": system_prompt, "type": "text"}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "auto"
                        }
                    }
                ]
            }
        ]
        
        return messages

    def analyze_image(
        self,
        image_path: str,
        system_prompt: str = "请精简、仔细描述一下这个图片，200字以内。",
        stream: bool = True,
        **kwargs
    ) -> ChatMessage:
        """
        分析图像内容
        
        Args:
            image_path: 图像文件路径
            system_prompt: 系统提示词
            stream: 是否流式输出
            **kwargs: 其他参数
            
        Returns:
            ChatMessage: 模型返回的消息
        """
        messages = self.prepare_image_message(image_path, system_prompt)
        return self(messages=messages, **kwargs)