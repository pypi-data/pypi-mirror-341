"""This module provides a toolkit for interacting with the ZMP API."""

from __future__ import annotations

import logging
from typing import List

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit
from zmp_openapi_helper.models.operation import ZmpAPIOperation
from zmp_openapi_helper.wrapper.api_wrapper import ZmpAPIWrapper

from zmp_openapi_toolkit.tools.tool import ZmpTool

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZmpToolkit(BaseToolkit):
    """Toolkit for interacting with the ZMP API."""

    tools: List[BaseTool] = []

    @classmethod
    def from_zmp_api_wrapper(cls, *, zmp_api_wrapper: ZmpAPIWrapper) -> ZmpToolkit:
        """Create ZMP toolkit from ZMP API wrapper.

        Args:
            zmp_api_wrapper (BaseAPIWrapper): ZMP API wrapper

        Returns:
            ZmpToolkit: ZMP toolkit
        """
        operations: List[ZmpAPIOperation] = zmp_api_wrapper.get_operations()

        tools = [
            ZmpTool(
                name=operation.name,
                description=operation.description,
                args_schema=operation.args_schema,
                method=operation.method,
                path=operation.path,
                path_params=operation.path_params,
                query_params=operation.query_params,
                request_body=operation.request_body,
                api_wrapper=zmp_api_wrapper,
            )
            for operation in operations
        ]

        log_str = "\nTools for LLM:\n"
        log_str += ("=" * 100) + "\n"
        for i, tool in enumerate(tools):
            log_str += f"Tool [{i}]\n"
            log_str += "-" * 100 + "\n"
            log_str += f"  Name: {tool.name}\n"
            log_str += f"  Description: {tool.description[:100] + '...(Omitted)' if len(tool.description) > 100 else tool.description}\n"
            log_str += f"  Args schema: {tool.args_schema}\n"
            for field_name, field_info in tool.args_schema.model_fields.items():
                log_str += (
                    f"    {field_name}: {field_info.annotation} {field_info.default}\n"
                )
            log_str += f"  Method: {tool.method}\n"
            log_str += f"  Path: {tool.path}\n"
            log_str += f"  Path params: {tool.path_params}\n"
            log_str += f"  Query params: {tool.query_params}\n"
            if tool.query_params:
                for field_name, field_info in tool.query_params.model_fields.items():
                    log_str += f"    {field_name}: {field_info.annotation} {field_info.default}\n"
            log_str += f"  Request body: {tool.request_body}\n"
            log_str += f"  API wrapper: {tool.api_wrapper}\n"

        log_str += ("=" * 100) + "\n"
        logger.info(log_str)

        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get tools from the toolkit."""
        return self.tools
