# tools.py（保持不变）
from . import app

@app.tool()
async def mcp_add(a: int, b: int) -> int:
    return a + b