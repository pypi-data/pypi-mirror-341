from fastapi import APIRouter, HTTPException, Request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from abc import ABC, abstractmethod
import os
import json
import uuid
from typing import Dict, Any
from pathlib import Path
from botrun_flow_lang.langgraph_agents.agents.agent_runner import agent_runner
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import (
    SearchAgentGraph,
    DEFAULT_SEARCH_CONFIG
)
from botrun_flow_lang.langgraph_agents.agents.checkpointer.firestore_checkpointer import AsyncFirestoreCheckpointer
from botrun_flow_lang.utils.langchain_utils import litellm_msgs_to_langchain_msgs
import asyncio


# 讀取 system prompt
current_dir = Path(__file__).parent
SUBSIDY_API_SYSTEM_PROMPT = (
    current_dir / "subsidy_api_system_prompt.txt"
).read_text(encoding="utf-8")

# LINE 訊息長度限制
MAX_MESSAGE_LENGTH = 5000


def get_subsidy_bot_search_config(stream: bool = True) -> dict:
    return {
        **DEFAULT_SEARCH_CONFIG,
        "search_prompt": SUBSIDY_API_SYSTEM_PROMPT,
        "related_prompt": "",
        "domain_filter": ["*.gov.tw", "-*.gov.cn"],
        "user_prompt_prefix": "你是台灣人，你不可以講中國用語也不可以用簡體中文，禁止！你的回答內容不要用Markdown格式。",
        "stream": stream
    }


class LineBotBase(ABC):
    """LINE Bot 基礎類別，定義共用功能和介面

    此類別提供 LINE Bot 的基本功能，包含：
    1. Webhook 處理和驗證
    2. 訊息接收和回覆
    3. 定義訊息回覆邏輯介面

    所有的 LINE Bot 實作都應該繼承此類別並實作 get_reply_text 方法。
    """

    def __init__(self, channel_secret: str, channel_access_token: str):
        """初始化 LINE Bot 設定

        Args:
            channel_secret (str): LINE Channel Secret，用於驗證 webhook 請求
            channel_access_token (str): LINE Channel Access Token，用於發送訊息給使用者

        Raises:
            ValueError: 當 channel_secret 或 channel_access_token 為空時
        """
        if not channel_secret or not channel_access_token:
            raise ValueError("LINE Bot channel_secret 和 channel_access_token 不能為空")

        self.handler = WebhookHandler(channel_secret)
        self.configuration = Configuration(access_token=channel_access_token)

        # 註冊訊息處理函數到 LINE Bot SDK
        # 使用 lambda 避免 SDK 傳入多餘的 destination 參數，並用 asyncio.create_task 處理非同步函數
        # MessageEvent: 訊息事件
        # message=TextMessageContent: 指定處理文字訊息
        self.handler.add(MessageEvent, message=TextMessageContent)(
            lambda event: asyncio.create_task(self.handle_message(event))
        )

    async def callback(self, request: Request) -> Dict[str, Any]:
        """處理來自 LINE Platform 的 webhook 回調請求

        驗證請求簽章並處理訊息事件。所有接收到的 webhook 內容都會被記錄。

        Args:
            request (Request): FastAPI 請求物件，包含 webhook 請求的內容

        Returns:
            Dict[str, Any]: 包含處理結果的回應，成功時回傳 {"success": True}

        Raises:
            HTTPException: 當請求簽章驗證失敗時，回傳 400 狀態碼
        """
        signature = request.headers.get("X-Line-Signature", "")
        body = await request.body()
        body_str = body.decode("utf-8")

        try:
            self.handler.handle(body_str, signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")

        body_json = json.loads(body_str)
        print("Received webhook:", json.dumps(body_json, indent=2, ensure_ascii=False))

        return {"success": True}

    async def handle_message(self, event: MessageEvent) -> None:
        """處理收到的文字訊息並發送回覆

        此方法會：
        1. 記錄收到的訊息和發送者資訊
        2. 使用 get_reply_text 取得回覆內容
        3. 發送回覆訊息給使用者，如果訊息過長會分段發送

        Args:
            event (MessageEvent): LINE 訊息事件，包含訊息內容和發送者資訊
        """
        print(f"Received message from {event.source.user_id}: {event.message.text}")
        reply_text = await self.get_reply_text(event.message.text, event.source.user_id)

        print(f"Total response length: {len(reply_text)}")

        # 將長訊息分段，每段不超過 MAX_MESSAGE_LENGTH
        message_chunks = []
        remaining_text = reply_text

        while remaining_text:
            # 如果剩餘文字長度在限制內，直接加入並結束
            if len(remaining_text) <= MAX_MESSAGE_LENGTH:
                message_chunks.append(remaining_text)
                print(f"Last chunk length: {len(remaining_text)}")
                break

            # 確保分段大小在限制內
            safe_length = min(
                MAX_MESSAGE_LENGTH - 100, len(remaining_text)
            )  # 預留一些空間

            # 在安全長度內尋找最後一個完整句子
            chunk_end = safe_length
            for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                if remaining_text[i] in "。！？!?":
                    chunk_end = i + 1
                    break

            # 如果找不到適合的句子結尾，就用空格或換行符號來分割
            if chunk_end == safe_length:
                for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                    if remaining_text[i] in " \n":
                        chunk_end = i + 1
                        break
                # 如果還是找不到合適的分割點，就直接在安全長度處截斷
                if chunk_end == safe_length:
                    chunk_end = safe_length

            # 加入這一段文字
            current_chunk = remaining_text[:chunk_end]
            print(f"Current chunk length: {len(current_chunk)}")
            message_chunks.append(current_chunk)

            # 更新剩餘文字
            remaining_text = remaining_text[chunk_end:]

        print(f"Number of chunks: {len(message_chunks)}")
        for i, chunk in enumerate(message_chunks):
            print(f"Chunk {i} length: {len(chunk)}")

        # 使用 LINE Messaging API 發送回覆
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            messages = [TextMessage(text=chunk) for chunk in message_chunks]
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
            )

    @abstractmethod
    async def get_reply_text(self, line_user_message: str, user_id: str) -> str:
        """根據收到的訊息決定回覆內容

        此方法需要被子類別實作，定義 bot 的回覆邏輯。

        Args:
            line_user_message (str): 使用者傳送的 LINE 訊息內容
            user_id (str): 使用者的 LINE ID，可用於個人化回覆或追蹤使用者狀態

        Returns:
            str: 要回覆給使用者的訊息內容
        """
        pass


# 建立 subsidy_line_bot 專用的 SearchAgentGraph 實例
env_name = os.getenv("ENV_NAME", "botrun-flow-lang-dev")
subsidy_line_bot_graph = SearchAgentGraph(
    memory=AsyncFirestoreCheckpointer(env_name=env_name)
).graph

class SubsidyLineBot(LineBotBase):
    """波津貼 LINE Bot 實作"""

    async def get_reply_text(self, line_user_message: str, user_id: str) -> str:
        """實作波津貼 LINE Bot 的回覆邏輯

        使用 agent_runner 處理使用者訊息並回傳回覆內容

        Args:
            line_user_message (str): 使用者傳送的 LINE 訊息內容
            user_id (str): 使用者的 LINE ID

        Returns:
            str: 回覆訊息
        """
        # 準備訊息格式
        messages = [
            {"role": "system", "content": SUBSIDY_API_SYSTEM_PROMPT},
            {"role": "user", "content": line_user_message},
        ]
        messages_for_langchain = litellm_msgs_to_langchain_msgs(messages)

        # 使用 agent_runner 處理訊息，使用 LINE user_id 作為對話追蹤識別碼
        full_response = ""
        async for event in agent_runner(
            user_id, 
            {"messages":[line_user_message]}, 
            subsidy_line_bot_graph,
            extra_config=get_subsidy_bot_search_config()
        ):
            full_response += event.chunk

        # 移除sonar-reasoning-pro模型的思考過程內容
        if "</think>" in full_response:
            full_response = full_response.split("</think>", 1)[1]

        return full_response


# 初始化 FastAPI 路由器，設定 API 路徑前綴
router = APIRouter(prefix="/line_bot")


# 初始化波津貼 LINE Bot 實例
def get_subsidy_bot():
    # 使用環境變數取得 LINE Bot 的驗證資訊
    return SubsidyLineBot(
        channel_secret=os.getenv("SUBSIDY_LINE_BOT_CHANNEL_SECRET"),
        channel_access_token=os.getenv("SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN"),
    )


@router.post("/subsidy/webhook")
async def subsidy_webhook(request: Request):
    """波津貼Line bot的webhook endpoint"""
    return await get_subsidy_bot().callback(request)
