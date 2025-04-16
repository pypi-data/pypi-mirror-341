"""This module provides a tool for interacting with the ZMP API."""

import logging
from typing import Any, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from zmp_openapi_helper.wrapper.api_wrapper import ZmpAPIWrapper

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZmpTool(BaseTool):
    """Tool for interacting with the ZMP API.

    This tool provides an interface to execute operations against a ZMP API endpoint.
    It supports different modes of operation and can handle both schema-validated
    and raw instruction inputs.

    Attributes:
        mode (str): The operation mode to execute
        name (str): Display name of the tool
        method (str): The HTTP method to use
        path (str): The path to the resource
        description (str): Detailed description of what the tool does
        path_params (Optional[Type[BaseModel]]): Path parameters for the tool
        query_params (Optional[Type[BaseModel]]): Query parameters for the tool
        request_body (Optional[Type[BaseModel]]): Request body for the tool
        api_wrapper (BaseAPIWrapper): The wrapper instance for making API calls
    """

    api_wrapper: ZmpAPIWrapper = Field(default_factory=ZmpAPIWrapper)

    method: str = Field(..., description="The HTTP method to use")
    path: str = Field(..., description="The path to the resource")
    path_params: Optional[Type[BaseModel]] = Field(
        None, description="Path parameters for the tool"
    )
    query_params: Optional[Type[BaseModel]] = Field(
        None, description="Query parameters for the tool"
    )
    request_body: Optional[Type[BaseModel]] = Field(
        None, description="Request body for the tool"
    )

    def _run(
        self,
        instructions: Optional[str] = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the ZCP tool with the given instructions.

        Args:
            instructions (Optional[str], optional): Instructions or parameters to pass to the ZCP API. Defaults to "".
            run_manager (Optional[CallbackManagerForToolRun], optional): Callback manager for the tool run. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the API wrapper.

        Returns:
            str: Response from the ZCP API after executing the instructions.
        """
        logger.info("-" * 100)
        logger.info("kwargs from LLM:")
        for key, value in kwargs.items():
            logger.info(f"  {key}: {value}")
        logger.info("-" * 100)

        if not instructions or instructions == "{}":
            instructions = ""

        if self.path_params is not None:
            path_params = self.path_params(**kwargs)
            logger.debug(f"Path params: {path_params}")
        else:
            path_params = None

        if self.query_params is not None:
            query_params = self.query_params(**kwargs)
            logger.debug(f"Query params: {query_params}")
        else:
            query_params = None

        if self.request_body is not None:
            request_body = self.request_body(**kwargs)
            logger.debug(f"Request body type: {type(request_body)}")
        else:
            request_body = None

        return self.api_wrapper.run(
            self.method,
            self.path,
            path_params=path_params,
            query_params=query_params,
            request_body=request_body,
        )
