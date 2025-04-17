import os

from openai.types.beta import FunctionToolParam
from openai.types.shared_params import FunctionDefinition
from openai.types.beta.threads.required_action_function_tool_call import (
    RequiredActionFunctionToolCall,
)
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput


from knit_openai.exceptions.exceptions import InvalidKnitAPIKey
from knit_openai.models.tools_filter import ToolFilter
from knit_openai.models.tools_summary import ToolSummary
from knit_openai.utils.constants import ENVIRONMENT_PRODUCTION
from knit_openai.client.http_client import HTTPClient
from knit_openai.client.auth_client import AuthClient
from knit_openai.logger import knit_logger


class KnitOpenAI:
    """
    A client for interfacing with the Knit OpenAI integration.

    This client handles authentication and manages interactions with the Knit API
    for OpenAI integrations, allowing tool discovery and execution with OpenAI assistants.
    """

    _api_key: str
    _http_client: HTTPClient = None
    _auth_client: AuthClient = None
    integration_id: str
    environment: str = ENVIRONMENT_PRODUCTION

    def __init__(
        self,
        api_key: str | None = None,
        integration_id: str | None = None,
        environment: str | None = None,
    ):
        """
        Initialize a new instance of the KnitOpenAI client.

        Args:
            api_key (str, optional): The API key used for authenticating requests.
                If not provided, it will attempt to read from the KNIT_API_KEY environment variable.
            integration_id (str, optional): The integration ID associated with this client.
            environment (str, optional): The API environment to connect to, defaulting to production if not specified.

        Raises:
            InvalidKnitAPIKey: If the api_key is not provided either by argument or environment variable.
        """
        knit_logger.debug("Initializing KnitOpenAI client")

        if api_key is None:
            knit_logger.debug("API key not provided, checking environment variable")
            api_key = os.environ.get("KNIT_API_KEY")

        if api_key is None:
            knit_logger.error(
                "API key not found in environment variable or constructor argument"
            )
            raise InvalidKnitAPIKey(
                "The api_key must be set either by passing api_key to the SDK or by setting the KNIT_API_KEY environment variable"
            )
        self._api_key = api_key

        self.environment = environment
        self.integration_id = integration_id
        knit_logger.debug(
            "KnitOpenAI client initialized with environment: %s, integration_id: %s",
            environment,
            integration_id,
        )

        self.auth_client.initialize_sdk(self)
        knit_logger.debug("Auth client initialized")

    @property
    def auth_client(self) -> AuthClient:
        """
        Get the authentication client for managing API interactions.

        If the authentication client has not been instantiated, it creates one.

        Returns:
            AuthClient: The authentication client instance for handling authorization.
        """
        if not self._auth_client:
            knit_logger.debug("Creating new AuthClient instance")
            self._auth_client = AuthClient()

        return self._auth_client

    @property
    def api_key(self) -> str:
        """
        Get the API key used for authenticating requests.

        Returns:
            str: The API key.

        Raises:
            InvalidKnitAPIKey: If the API key is not set.
        """
        if not self._api_key:
            knit_logger.error("API key not set when attempting to access it")
            raise InvalidKnitAPIKey(
                "The api_key must be set either by passing api_key to the SDK or by setting the KNIT_API_KEY environment variable"
            )
        return self._api_key

    @property
    def http_client(self) -> HTTPClient:
        """
        Get the HTTP client for making API requests.

        If the HTTP client hasn't been instantiated, it creates one using the current environment setting.

        Returns:
            HTTPClient: The HTTP client instance for handling requests.
        """
        if not self._http_client:
            knit_logger.debug(
                "Creating new HTTPClient instance with environment: %s",
                self.environment,
            )
            self._http_client = HTTPClient(self.environment)

        return self._http_client

    def find_tools(
        self,
        app_id: str | None = None,
        entities: list[str] | None = None,
        operation: str | None = None,
        category_id: str | None = None,
        include_unified_tools: bool = False,
        usecase: str | None = None,
    ) -> list[ToolSummary]:
        """
        Find and retrieve a list of tool summaries based on specified filters.

        This method fetches tools that match given criteria and returns them as ToolSummary objects.

        Args:
            app_id (str, optional): The application ID for which tools are being retrieved.
            entities (list[str], optional): A list of entities to filter the tools.
            operation (str, optional): An operation name to filter the tools.
                Allowed values are "read" and "write".
            category_id (str, optional): A category ID to filter the tools.
                Must be specified if app_id is not provided.
            include_unified_tools (bool, optional): Whether to include unified tools.
                Defaults to False.
            usecase (str, optional): Search for tools by semantic search.

        Returns:
            list[ToolSummary]: A list of ToolSummary objects representing the tools
                that match the specified filters.

        Raises:
            Exception: If an error occurs during the API request.
        """
        knit_logger.debug(
            "Finding tools with filters - app_id: %s, entities: %s, operation: %s, category_id: %s, include_unified_tools: %s, usecase: %s",
            app_id,
            entities,
            operation,
            category_id,
            include_unified_tools,
            usecase,
        )

        filter_obj = {
            **({"app_id": app_id} if app_id is not None else {}),
            **({"entities": entities} if entities is not None else {}),
            **({"operation": operation} if operation is not None else {}),
            **({"category_id": category_id} if category_id is not None else {}),
            **({"usecase": usecase} if usecase is not None else {}),
            **(
                {"include_unified_tools": include_unified_tools}
                if include_unified_tools
                else {}
            ),
        }

        try:
            knit_logger.debug(
                "Sending request to /tools.find with filters: %s", filter_obj
            )
            response = self.http_client.send_request(
                instance=self,
                url="/tools.find",
                method="GET",
                validate_response=True,
                params=None,
                json_body={"filters": filter_obj},
            )

            data = response.json()["data"]
            knit_logger.debug("Retrieved %d tools from /tools.find", len(data))

            tools = []
            for tool in data:
                tools.append(
                    ToolSummary(
                        tool_id=tool["tool_id"],
                        entities=tool["entities"],
                        operation=tool["operation"],
                        title=tool["title"],
                        description=tool["description"],
                    )
                )

            return tools
        except Exception as e:
            knit_logger.error("Error finding tools: %s", str(e))
            raise

    def get_tools(self, tools: list[ToolFilter]) -> list[FunctionToolParam]:
        """
        Retrieve a list of tools based on the specified filters.

        This method fetches tools matching the given filters and converts them to
        OpenAI's FunctionToolParam objects that can be used with OpenAI assistants.

        Args:
            tools (list[ToolFilter]): A list of ToolFilter objects representing the
                criteria for tools to retrieve.

        Returns:
            list[FunctionToolParam]: A list of OpenAI's FunctionToolParam objects representing
                the tools that match the specified filters.

        Raises:
            Exception: If an error occurs during the API request or tool processing.
        """
        knit_logger.debug("Getting tools with %d filter(s)", len(tools))

        filter_obj = [tool.model_dump(exclude_none=True) for tool in tools]
        knit_logger.debug("Tool filters: %s", filter_obj)

        try:
            knit_logger.debug("Sending request to /tools.openai.get")
            response = self.http_client.send_request(
                instance=self,
                url="/tools.openai.get",
                method="POST",
                validate_response=True,
                params=None,
                json_body={"filters": filter_obj},
            )

            data = response.json()["data"]
            knit_logger.debug("Retrieved %d tools from /tools.openai.get", len(data))

            tools = []
            for tool in data:
                knit_logger.debug("Processing tool: %s", tool["name"])
                function_def = FunctionToolParam(
                    function=FunctionDefinition(
                        {
                            "name": tool["name"],
                            "description": tool.get("description", ""),
                            "parameters": tool.get("parameters", {}),
                        }
                    ),
                    type="function",
                )

                tools.append(function_def)
                knit_logger.debug("Added tool: %s", tool["name"])

            return tools
        except Exception as e:
            knit_logger.error("Error getting tools: %s", str(e))
            raise

    def handle_tool_call(
        self,
        tool_call: RequiredActionFunctionToolCall,
        knit_integration_id: str | list[str],
    ) -> ToolOutput:
        """
        Handle the execution of a tool call and return its output.

        This method processes a function tool call from OpenAI's assistant API,
        sends the request to the Knit API for execution, and returns the tool output
        in the format expected by OpenAI.

        Args:
            tool_call (RequiredActionFunctionToolCall): The tool call object from OpenAI's assistant,
                containing the function name and arguments to be executed.
            knit_integration_id (str, optional): The integration ID to use for executing the tool call.
                If not provided, the instance's integration_id will be used.

        Returns:
            ToolOutput: An object containing the tool call ID and the output from the tool execution.

        Raises:
            Exception: If an error occurs during the API request or tool execution.
        """
        function_name = tool_call.function.name
        knit_logger.debug(
            "Handling tool call - function: %s, tool_call_id: %s, knit_integration_id: %s",
            function_name,
            tool_call.id,
            knit_integration_id,
        )

        body = {
            "function_id": function_name,
            "arguments": tool_call.function.arguments,
            "knit_integration_id": knit_integration_id,
        }

        try:
            knit_logger.debug(
                "Sending request to /tools.openai.execute with body: %s", body
            )
            response = self.http_client.send_request(
                instance=self,
                url="/tools.openai.execute",
                method="POST",
                validate_response=True,
                params=None,
                json_body=body,
                knit_integration_id=None,
            )

            data = response.json()["data"]
            knit_logger.debug(
                "Tool execution completed for function: %s, result length: %d",
                function_name,
                len(str(data["toolOutput"])),
            )

            return ToolOutput(tool_call_id=tool_call.id, output=data["toolOutput"])
        except Exception as e:
            knit_logger.error(
                "Error executing tool call for function %s: %s", function_name, str(e)
            )
            raise
