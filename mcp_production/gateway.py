# gateway.py
import os
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# 本機跑：預設連 localhost
# Docker 裡：用環境變數 FINANCE_URL / KNOWLEDGE_URL 改成 http://finance:8001/mcp ...
FINANCE_URL = os.getenv("FINANCE_URL", "http://127.0.0.1:8001/mcp")
KNOWLEDGE_URL = os.getenv("KNOWLEDGE_URL", "http://127.0.0.1:8002/mcp")

gateway = FastMCP("EnterpriseGateway")

finance_proxy = FastMCP.as_proxy(
    ProxyClient(FINANCE_URL),
    name="FinanceProxy",
)

knowledge_proxy = FastMCP.as_proxy(
    ProxyClient(KNOWLEDGE_URL),
    name="KnowledgeProxy",
)

gateway.mount(finance_proxy, prefix="finance")
gateway.mount(knowledge_proxy, prefix="knowledge")
# tools e.g. finance_get_price, knowledge_search_faq

if __name__ == "__main__":
    gateway.run(
        transport="streamable-http",
        host="0.0.0.0",   # 容器裡對外
        port=9000,
        path="/mcp",
    )

