from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os
import uvicorn
import scanpy as sc
from .tool.io import io_tools, run_io_func
from .tool.pp import pp_tools, run_pp_func
from .tool.util import util_tools, run_util_func
from .tool.tl import tl_tools, run_tl_func
from .tool.pl import pl_tools, run_pl_func
from .util import get_figure
from .logging_config import setup_logger

logger = setup_logger(log_file=os.environ.get("SC_MCP_LOG_FILE", None))

class AdataState:
    def __init__(self):
        data_path = os.environ.get("SC_MCP_DATA", None)        
        if data_path:
            self.adata = sc.read_h5ad(data_path)
            logger.info(f"Data path: {data_path}")
        else:            
            self.adata = None
        
ads = AdataState()

MODULE = os.environ.get("SC_MCP_MODULE", "all")       

server = Server(f"scanpy-mcp-{MODULE}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    if MODULE == "io":
        tools = io_tools.values()
    elif MODULE == "pp":
        tools = pp_tools.values()
    elif MODULE == "tl":
        tools = tl_tools.values()
    elif MODULE == "pl":
        tools = pl_tools.values()
    elif MODULE == "util":
        tools = util_tools.values()
    else:
        tools = [
            *io_tools.values(),
            *pp_tools.values(),
            *tl_tools.values(),
            *pl_tools.values(),
            *util_tools.values(),
        ]
    return tools


@server.call_tool()
async def call_tool(
    name: str, arguments
):
    try:
        logger.info(f"Running {name} with {arguments}")
        if name in io_tools.keys():
            #logger.info(f"Runing {name} at {arguments}")
            res = run_io_func(ads.adata, name, arguments)
            ads.adata = res
        elif name in pp_tools.keys():
            #logger.info(f"Runing {name} at {arguments}")
            res = run_pp_func(ads.adata, name, arguments)
        elif name in tl_tools.keys():
            res = run_tl_func(ads.adata, name, arguments) 
        elif name in pl_tools.keys():
            logger.info(f"Runing {name} at ")
            import base64
            from mcp.types import ImageContent
            from mcp.server.fastmcp import Image
            res = run_pl_func(ads.adata, name, arguments)
            # try:
            #     data = base64.b64encode(img).decode()
            #     res = ImageContent(type="image", data=data, mimeType="image/png")
            #     return [res]
            # except Exception as e:
            #     logger.info(f"Error converting figure to bytes: {e}")
            #     raise e
            # return res

        elif name in util_tools.keys():
            
            res = run_util_func(ads.adata, name, arguments)

        output = str(res) if res is not None else str(ads.adata)
        return [
            types.TextContent(
                type="text",
                text=str({"output": output})
            )
        ]
    except Exception as error:
        logger.error(f"{name} with {error}")
        return [
            types.TextContent(
                type="text",
                text=str({"Error": error})
            )
        ]


        
## Run server with stdio transport
async def run_stdio():
    """
    Run server with stdio transport
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=f"scmcp-{MODULE}",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

## Create application using SSE transport
def create_sse_app(port=8000):
    """
    Create application using SSE transport
    
    Parameters:
        port: Server port number
        
    Returns:
        Starlette application instance
    """
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount
    from starlette.requests import Request
    from mcp.server.sse import SseServerTransport
    
    # Create SSE transport object
    sse = SseServerTransport("/messages/")

    # Define SSE handler function
    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], 
                InitializationOptions(
                    server_name=f"sc-mcp-{MODULE}",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                )
            )

    # Create Starlette application
    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
            Route("/figures/{figure_name}", endpoint=get_figure),
        ]
    )
    
    return starlette_app

# Keep the original run function as a compatibility layer
async def run(transport_type="stdio", port=8000):
    """
    Unified server run function (for backward compatibility)
    
    Parameters:
        transport_type: Transport type, either "stdio" or "sse"
        port: Port number when using sse transport
    """
    if transport_type == "stdio":
        await run_stdio()
    elif transport_type == "sse":
        return create_sse_app(port)
    else:
        raise ValueError(f"Unsupported transport type: {transport_type}")
