import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio


GATEWAY_URL = "http://127.0.0.1:9000/mcp"

# 確保有 OPENAI_API_KEY（如果你已經在 Colab 的環境變數設定過，可以省略這段）
os.environ["OPENAI_API_KEY"] = "sk-proj--"


async def main():
    # 1. 連到 FastMCP Gateway（multi-server proxy）
    async with streamablehttp_client(GATEWAY_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. 把 MCP tools 轉成 LangChain tools
            tools = await load_mcp_tools(session)
            print("Loaded tools:", [t.name for t in tools])

            # 3. 用你熟悉的 ChatOpenAI 寫法
            llm = ChatOpenAI(
                model="gpt-4.1",
                temperature=0.0,
            )

            # 4. 建 LangGraph 的 ReAct Agent（用 llm instance，而不是字串）
            agent = create_react_agent(
                model=llm,
                tools=tools,
                # 也可以加 prompt="You are a helpful assistant" 之類的自訂 system prompt
            )

            # 5. 測試：金融查詢（會走 finance_* MCP 工具）
            query_1 = "請幫我查一下 2330.TW 現在股價，順便說明最近一週的走勢。"
            result_1 = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": query_1}
                ]
            })
            print("\n=== 回覆一 ===")
            print(result_1["messages"][-1].content)

            # 6. 測試：FAQ / 內部知識（會走 knowledge_* MCP 工具）
            query_2 = "如果我要開證券戶，大概要多久？有沒有風險等級的說明？"
            result_2 = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": query_2}
                ]
            })
            print("\n=== 回覆二 ===")
            print(result_2["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
