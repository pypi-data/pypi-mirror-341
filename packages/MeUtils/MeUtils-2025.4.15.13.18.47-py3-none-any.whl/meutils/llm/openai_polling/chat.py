#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/4/10 16:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_base64
from meutils.llm.clients import AsyncOpenAI, zhipuai_client
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import CompletionRequest

from meutils.apis.proxy.kdlapi import get_one_proxy


class Completions(object):

    def __init__(
            self,
            base_url: Optional[str] = None,
            api_key: Optional[str] = None,
            http_client: Optional[httpx.AsyncClient] = None
    ):
        self.base_url = base_url
        self.api_key = api_key

        self.client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key, http_client=http_client)

    async def create(self, request: CompletionRequest):

        ###########################################################################

        # 开启视觉模型
        if not any(i in request.model for i in ["vl", 'vision']) and (urls := request.last_urls.get("image_url")):
            # logger.debug(request)
            if request.model.startswith(("gemini",)):  # 仅支持base64
                base64_list = await to_base64(urls, content_type="image/png")  ######## todo: tokens怎么计算的
                request.messages = [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': request.last_user_content
                            },
                            *[
                                {
                                    'type': 'image_url',
                                    'image_url': {
                                        'url': base64_data
                                    }
                                }
                                for base64_data in base64_list
                            ]

                        ]
                    }
                ]
            else:
                # logger.debug('xxxxxxxx')
                request.model = "glm-4v-flash"
                self.client = zhipuai_client
        ###########################################################################

        data = to_openai_params(request)
        if 'gemini' in request.model:
            data.pop("seed", None)
            data.pop("presence_penalty", None)
            data.pop("frequency_penalty", None)
            data.pop("extra_body", None)

        return await self.client.chat.completions.create(**data)


if __name__ == '__main__':
    # 测试 token 1800

    request = CompletionRequest(
        # model="gemini-2.0-flash",
        model="glm-4-flash",

        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "你是一个数学助手，擅长解决复杂的数学问题。"
                    }
                ]
            },
            # {"role": "user", "content": "你好"},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "解释下"
                },
                {
                    "image_url": {
                        "detail": "auto",
                        "url": "https://osshk.share704.com/file/upload/2025/04/14/1911575959253815296.jpg"
                    },
                    "type": "image_url"
                }
            ]}
        ],
        stream=False,
        max_tokens=8000,
    )
    arun(Completions().create(request))
