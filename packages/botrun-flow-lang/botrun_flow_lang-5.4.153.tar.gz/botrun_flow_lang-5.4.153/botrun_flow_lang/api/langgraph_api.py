import logging
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import time
from fastapi.responses import StreamingResponse
import json
from langgraph.errors import GraphRecursionError
import anthropic
import random
from litellm.types.utils import Choices
from botrun_flow_lang.constants import ERR_GRAPH_RECURSION_ERROR
from botrun_flow_lang.langgraph_agents.agents.agent_runner import (
    OnNodeStreamEvent,
    agent_runner,
    langgraph_runner,
)
from botrun_flow_lang.langgraph_agents.agents.langgraph_react_agent import (
    create_react_agent_graph,
    get_react_agent_model_name,
)
from botrun_flow_lang.models.token_usage import TokenUsage
from botrun_flow_lang.utils.botrun_logger import BotrunLogger, default_logger

from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import (
    SearchAgentGraph,
    # graph as search_agent_graph,
)

# from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.agent import (
#     graph as ai_researcher_graph,
# )
# from botrun_flow_lang.langgraph_agents.agents.open_deep_research.open_deep_research_graph import (
#     graph as deep_research_graph,
# )
from botrun_flow_lang.utils.langchain_utils import (
    extract_token_usage_from_state,
    langgraph_event_to_json,
    litellm_msgs_to_langchain_msgs,
)

router = APIRouter(prefix="/langgraph")


class LangGraphRequest(BaseModel):
    graph_name: str
    # todo LangGraph 應該要傳 thread_id，但是因為現在是 cloud run 的架構，所以 thread_id 不一定會讀的到 (auto scale)
    thread_id: Optional[str] = None
    user_input: Optional[str] = None
    messages: List[Dict[str, Any]] = []
    config: Optional[Dict[str, Any]] = None
    stream: bool = False
    # LangGraph 是否需要從 checkpoint 恢復
    need_resume: bool = False
    session_id: Optional[str] = None


class LangGraphResponse(BaseModel):
    """
    @param content: 這個是給評測用來評估結果用的
    @param state: 這個是graph的 final state，如果需要額外資訊可以使用
    @param token_usage: Token usage information for the entire graph execution
    """

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    content: Optional[str] = None
    state: Optional[Dict[str, Any]] = None
    token_usage: Optional[TokenUsage] = None


class SupportedGraphsResponse(BaseModel):
    """Response model for listing supported graphs"""

    graphs: List[str]


PERPLEXITY_SEARCH_AGENT = "perplexity_search_agent"
CUSTOM_WEB_RESEARCH_AGENT = "custom_web_research_agent"
LANGGRAPH_REACT_AGENT = "langgraph_react_agent"
DEEP_RESEARCH_AGENT = "deep_research_agent"


SUPPORTED_GRAPH_NAMES = [
    PERPLEXITY_SEARCH_AGENT,
    LANGGRAPH_REACT_AGENT,
]


def get_supported_graphs():
    return {
        PERPLEXITY_SEARCH_AGENT: SearchAgentGraph().graph,
        LANGGRAPH_REACT_AGENT: create_react_agent_graph(),
        # CUSTOM_WEB_RESEARCH_AGENT: ai_researcher_graph,
        # DEEP_RESEARCH_AGENT: deep_research_graph,
    }


def get_graph(
    graph_name: str,
    config: Optional[Dict[str, Any]] = None,
    stream: bool = False,
    messages: Optional[List[Dict]] = [],
):
    if graph_name not in SUPPORTED_GRAPH_NAMES:
        raise ValueError(f"Unsupported graph from get_graph: {graph_name}")
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        graph = SearchAgentGraph().graph
        graph_config = {
            "search_prompt": config.get("search_prompt", ""),
            "model_name": config.get("model_name", "sonar-reasoning-pro"),
            "related_prompt": config.get("related_question_prompt", ""),
            "search_vendor": config.get("search_vendor", "perplexity"),
            "domain_filter": config.get("domain_filter", []),
            "user_prompt_prefix": config.get("user_prompt_prefix", ""),
            "stream": stream,
        }
    elif graph_name == LANGGRAPH_REACT_AGENT:
        graph_config = None

        system_prompt = config.get("system_prompt", "")
        if messages:
            for message in messages:
                if message.get("role") == "system":
                    system_prompt = message.get("content", "")
        graph = create_react_agent_graph(
            system_prompt=system_prompt,
            botrun_flow_lang_url=config.get("botrun_flow_lang_url", ""),
            user_id=config.get("user_id", ""),
            model_name=config.get("model_name", ""),
        )
    return graph, graph_config


def get_init_state(
    graph_name: str,
    user_input: str,
    config: Optional[Dict[str, Any]] = None,
    messages: Optional[List[Dict]] = [],
    enable_prompt_caching: bool = False,
):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        if len(messages) > 0:
            return {"messages": litellm_msgs_to_langchain_msgs(messages)}
        if config.get("user_prompt_prefix", ""):
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": config.get("user_prompt_prefix", "")
                        + "\n\n"
                        + user_input,
                    }
                ]
            }

        return {"messages": [user_input]}
    elif graph_name == CUSTOM_WEB_RESEARCH_AGENT:
        if len(messages) > 0:
            return {
                "messages": litellm_msgs_to_langchain_msgs(messages),
                "model": config.get("model", "anthropic"),
            }
        return {
            "messages": [user_input],
            "model": config.get("model", "anthropic"),
        }
    elif graph_name == LANGGRAPH_REACT_AGENT:
        if len(messages) > 0:
            new_messages = []
            for message in messages:
                if message.get("role") != "system":
                    new_messages.append(message)
            return {
                "messages": litellm_msgs_to_langchain_msgs(
                    new_messages, enable_prompt_caching
                )
            }
        else:
            return {
                "messages": [user_input],
            }
    elif graph_name == DEEP_RESEARCH_AGENT:
        if len(messages) > 0:
            return {
                "messages": litellm_msgs_to_langchain_msgs(messages),
                "topic": user_input,
            }
        return {
            "messages": [user_input],
            "topic": user_input,
        }
    raise ValueError(f"Unsupported graph from get_init_state: {graph_name}")


def get_content(graph_name: str, state: Dict[str, Any]):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        return state["messages"][-3].content
    elif graph_name == CUSTOM_WEB_RESEARCH_AGENT:
        content = state["answer"].get("markdown", "")
        content = content.replace("\\n", "\n")
        if state["answer"].get("references", []):
            references = "\n\n參考資料：\n"
            for reference in state["answer"]["references"]:
                references += f"- [{reference['title']}]({reference['url']})\n"
            content += references
        return content
    elif graph_name == DEEP_RESEARCH_AGENT:
        sections = state["sections"]
        sections_str = "\n\n".join(
            f"章節: {section.name}\n"
            f"描述: {section.description}\n"
            f"需要研究: {'是' if section.research else '否'}\n"
            for section in sections
        )
        sections_str = "預計報告結構：\n\n" + sections_str
        return sections_str
    else:
        messages = state["messages"]
        # Find the last human message
        last_human_idx = -1
        for i, msg in enumerate(messages):
            if msg.type == "human":
                last_human_idx = i

        # Combine all AI messages after the last human message
        ai_contents = ""
        for msg in messages[last_human_idx + 1 :]:
            if msg.type == "ai":
                if isinstance(msg.content, list):
                    ai_contents += msg.content[0].get("text", "")
                else:
                    ai_contents += msg.content

        return ai_contents


class LangGraphStreamChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[Choices]


@router.post("/run")
async def run_langgraph(request: LangGraphRequest):
    """
    執行指定的 LangGraph，支援串流和非串流模式

    Args:
        request: 包含 graph_name 和輸入數據的請求

    Returns:
        串流模式: StreamingResponse
        非串流模式: LangGraphResponse
    """
    try:
        graph, graph_config = get_graph(
            request.graph_name, request.config, request.stream
        )
        init_state = get_init_state(
            request.graph_name, request.user_input, request.config
        )

        if request.stream:
            return StreamingResponse(
                langgraph_stream_response(request.thread_id, init_state, graph),
                media_type="text/event-stream",
            )

        # 非串流模式的原有邏輯
        async for event in agent_runner(
            request.thread_id, init_state, graph, extra_config=graph_config
        ):
            pass

        config = {"configurable": {"thread_id": request.thread_id}}
        state = graph.get_state(config)
        content = get_content(request.graph_name, state.values)
        token_usage = extract_token_usage_from_state(state.values)
        return LangGraphResponse(
            id=request.thread_id,
            created=int(time.time()),
            model=request.graph_name,
            content=content,
            state=state.values,
            token_usage=token_usage,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"執行 LangGraph 時發生錯誤: {str(e)}"
        )


async def process_langgraph_request(
    request: LangGraphRequest,
    retry: bool = False,
    logger: logging.Logger = default_logger,
) -> None:
    """處理 LangGraph 請求的核心邏輯，包含錯誤處理和重試機制

    Args:
        request: LangGraph 請求
        retry: 是否為重試請求
        logger: 日誌記錄器，可以是任何 logging.Logger 的實例。
                預設使用 utils.botrun_logger.default_logger (標準 console logger)。

    Returns:
        LangGraphResponse 或 StreamingResponse
    """
    try:
        graph, graph_config = get_graph(
            request.graph_name, request.config, request.stream, request.messages
        )
        # user_input_model_name = request.config.get("model_name", "")
        init_state = get_init_state(
            request.graph_name,
            request.user_input,
            request.config,
            request.messages,
            False,
            # get_react_agent_model_name(user_input_model_name).startswith("claude-"),
        )
        thread_id = str(uuid.uuid4())
        if request.thread_id is not None:
            thread_id = request.thread_id

        logger.info(f"thread_id: {thread_id}")
        if request.stream:
            return StreamingResponse(
                langgraph_stream_response(
                    thread_id, init_state, graph, request.need_resume, logger
                ),
                media_type="text/event-stream",
            )

        # 非串流模式的原有邏輯
        logger.info("run agent_runner for request not stream")
        # todo stream模式的 need_resume 還沒有 測試，不知道效果
        async for event in agent_runner(
            thread_id,
            init_state,
            graph,
            request.need_resume,
            logger,
            extra_config=graph_config,
        ):
            pass
        logger.info("end run agent_runner for request not stream")
        config = {"configurable": {"thread_id": thread_id}}
        state = await graph.aget_state(config)
        try:
            logger.info(
                f"end state.values", values=langgraph_event_to_json(state.values)
            )
        except Exception as e:
            logger.error(f"end state.values error: {e}")
        content = get_content(request.graph_name, state.values)
        model_name = request.config.get("model_name", "")
        if request.graph_name == LANGGRAPH_REACT_AGENT:
            model_name = get_react_agent_model_name(model_name)
        token_usage = extract_token_usage_from_state(state.values, model_name)
        return LangGraphResponse(
            id=thread_id,
            created=int(time.time()),
            model=request.graph_name,
            content=content,
            state=state.values,
            token_usage=token_usage,
        )
    except anthropic.RateLimitError as e:
        # 如果是重試之後仍然發生 RateLimitError，則拋出異常
        if retry:
            import traceback

            traceback.print_exc()
            logger.error(
                "Retry failed with Anthropic RateLimitError",
                error=str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=500, detail=f"執行 LangGraph 時發生超過速率限制: {str(e)}"
            )
        # 第一次發生 RateLimitError，記錄並重試
        logger.info("Rate limit error occurred")
        # 隨機等待 7-20 秒
        retry_delay = random.randint(7, 20)
        logger.info(f"Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
        logger.info("Retrying after rate limit error...")
        # 重試
        return await process_langgraph_request(request, retry=True, logger=logger)
    except GraphRecursionError as e:
        logger.error(
            f"GraphRecursionError: {str(e)}",
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail=f"執行 LangGraph 時發生超過最大遞迴深度: {str(e)}"
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(
            f"process request get error Exception: {str(e)}",
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail=f"執行 LangGraph 時發生錯誤: {str(e)}"
        )


@router.post("/invoke")
async def invoke(request: LangGraphRequest):
    """
    執行指定的 LangGraph，支援串流和非串流模式

    Args:
        request: 包含 graph_name 和輸入數據的請求

    Returns:
        串流模式: StreamingResponse
        非串流模式: LangGraphResponse
    """
    session_id = request.session_id
    user_id = request.config.get("user_id", "")

    # *** Create a NEW BotrunLogger for this specific request ***
    # This ensures Cloud Logging and session/user context
    logger = BotrunLogger(session_id=session_id, user_id=user_id)

    logger.info(
        "invoke LangGraph API",
        request=request.model_dump(),
    )

    # Pass the request-specific BotrunLogger down
    return await process_langgraph_request(request, logger=logger)


async def langgraph_stream_response(
    thread_id: str,
    init_state: Dict,
    graph: Any,
    need_resume: bool = False,
    logger: logging.Logger = default_logger,
):
    try:
        logger.info(
            "start langgraph_stream_response",
            thread_id=thread_id,
            need_resume=need_resume,
        )
        final_event = None
        async for event in langgraph_runner(thread_id, init_state, graph, need_resume):
            final_event = event
            from datetime import datetime

            print(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                langgraph_event_to_json(event),
            )
            yield f"data: {langgraph_event_to_json(event)}\n\n"
        if final_event:
            logger.info(
                "end langgraph_stream_response",
                thread_id=thread_id,
                need_resume=need_resume,
                final_event=langgraph_event_to_json(final_event),
            )
        else:
            logger.info(
                "end langgraph_stream_response",
                thread_id=thread_id,
                need_resume=need_resume,
            )
        yield "data: [DONE]\n\n"
    except GraphRecursionError as e:
        logger.error(
            f"GraphRecursionError in stream: {str(e)} for thread_id: {thread_id}",
            error=str(e),
            exc_info=True,
        )
        try:
            error_msg = json.dumps(
                {
                    "error": ERR_GRAPH_RECURSION_ERROR,
                }
            )
            yield f"data: {error_msg}\n\n"
        except Exception as inner_e:
            logger.error(
                f"Error serializing GraphRecursionError message: {str(inner_e)} for thread_id: {thread_id}",
                error=str(inner_e),
                exc_info=True,
            )
            yield f"data: {json.dumps({'error': ERR_GRAPH_RECURSION_ERROR})}\n\n"
    except Exception as e:
        logger.error(
            f"Exception in stream: {str(e)} for thread_id: {thread_id}",
            error=str(e),
            exc_info=True,
        )
        error_response = {"error": str(e)}
        yield f"data: {json.dumps(error_response)}\n\n"


@router.get("/list", response_model=SupportedGraphsResponse)
async def list_supported_graphs():
    """
    列出所有支援的 LangGraph names

    Returns:
        包含所有支援的 graph names 的列表
    """
    return SupportedGraphsResponse(graphs=list(SUPPORTED_GRAPH_NAMES))
