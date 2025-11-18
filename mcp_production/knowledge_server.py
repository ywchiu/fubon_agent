# knowledge_server.py
from fastmcp import FastMCP

mcp = FastMCP("Knowledge")

FAKE_FAQ = {
    "開戶": "您可以透過線上表單或臨櫃開戶，平均作業時間約 3 個工作天。",
    "風險等級": "本公司會依照投資屬性問卷，將客戶區分為 5 個風險等級。",
}

@mcp.tool()
async def search_faq(query: str) -> str:
    """簡單 FAQ 查詢（示範用）"""
    for key, ans in FAKE_FAQ.items():
        if key in query:
            return ans
    return "暫時找不到相關 FAQ，請改用人工客服詢問。"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8002)

