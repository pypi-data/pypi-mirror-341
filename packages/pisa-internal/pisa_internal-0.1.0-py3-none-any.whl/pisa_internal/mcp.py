from typing import List
import os
from functools import partial

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool
import gradio_client


dynamic_data = {}

# Create an MCP server
app = FastMCP("galileo")

hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN is not set")

hf_space_client = gradio_client.Client("rungalileo/logstream-insights-demo", hf_token=hf_token)


def call_hf_endpoint(api_name: str, **kwargs):
    response = hf_space_client.predict(
        api_name=api_name,
        **kwargs,
    )
    return response


def get_tools(app):
    tool_code_response = hf_space_client.predict(
        api_name="/get_tools",
    )
    tool_code = tool_code_response["code"]

    exec(tool_code)

    return app


app = get_tools(app)

def main():
    app.run()
