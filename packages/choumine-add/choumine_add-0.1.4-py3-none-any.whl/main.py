from mcp.server import FastMCP


# 初始化 FastMCP 服务器
app = FastMCP('choumine-add')


@app.tool()
async def choumine_add(a: int, b: int) -> int:
    """计算两个数字的和并返回结果。

    参数:
        a: 第一个数字
        b: 第二个数字
    """
    return a+b


if __name__ == "__main__":
    app.run(transport='stdio')