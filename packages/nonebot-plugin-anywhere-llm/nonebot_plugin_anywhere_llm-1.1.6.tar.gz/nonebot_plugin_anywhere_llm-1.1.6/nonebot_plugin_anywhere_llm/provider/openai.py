from .interface import BaseLLMProvider
from ..config import LLMParams
from openai import APIError, APITimeoutError, AsyncOpenAI, AuthenticationError
from nonebot import  logger
from typing import Any, List, Tuple


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        ...
      
    async def generate(self, messages: List[Tuple[str, str]], params: LLMParams) -> str:
        
        self.client = AsyncOpenAI(
            api_key = params.api_key, 
            base_url = params.base_url
        )
        
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                model=params.model,
                max_tokens=params.max_tokens,
                frequency_penalty=params.frequency_penalty,
                presence_penalty=params.presence_penalty,
                stream=False
            )
            return response.choices[0].message.content
        
        except APITimeoutError as e:
            logger.error(f"API 请求超时: {e}")
            raise "⚠️请求超时，请重试"
        except APIError as e:
            logger.error(f"API 错误: {e.status_code} - {e.message}")
            raise "⚠️服务暂时不可用"
        except AuthenticationError:
            logger.critical("API 密钥错误")
            raise "⚠️服务配置错误"
        except Exception as e:
            logger.error(f"未处理异常: {e}")
            raise "⚠️服务内部错误"

openai_provider = OpenAIProvider()