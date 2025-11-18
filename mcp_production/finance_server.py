
# finance_server.py
from fastmcp import FastMCP

mcp = FastMCP("Finance")

@mcp.tool()
async def get_price(symbol: str) -> dict:
    """取得股票當前價格（示範用，回傳假資料）"""
    return {
        "symbol": symbol,
        "price": 999.5,
        "currency": "TWD",
    }

@mcp.tool()
async def get_week_summary(symbol: str) -> str:
    """取得最近一週走勢說明（示範用）"""
    return f"{symbol} 最近一週震盪走高，量能放大，請自行評估風險。"

if __name__ == "__main__":
    # 重要：在 Docker 裡用 0.0.0.0
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)

