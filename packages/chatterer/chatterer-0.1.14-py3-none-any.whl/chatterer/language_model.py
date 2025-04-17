import re
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Self,
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
    overload,
)

from langchain_core.language_models.base import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.utils.utils import secret_from_env
from pydantic import BaseModel, Field

from .messages import AIMessage, BaseMessage, HumanMessage, UsageMetadata
from .utils.code_agent import CodeExecutionResult, FunctionSignature, augment_prompt_for_toolcall

if TYPE_CHECKING:
    from instructor import Partial
    from langchain_experimental.tools.python.tool import PythonAstREPLTool

PydanticModelT = TypeVar("PydanticModelT", bound=BaseModel)
StructuredOutputType: TypeAlias = dict[object, object] | BaseModel

DEFAULT_IMAGE_DESCRIPTION_INSTRUCTION = "Provide a detailed description of all visible elements in the image, summarizing key details in a few clear sentences."
DEFAULT_CODE_GENERATION_PROMPT = (
    "You are utilizing a Python code execution tool now.\n"
    "Your goal is to generate Python code that solves the task efficiently and appends both the code and its output to your context memory.\n"
    "\n"
    "To optimize tool efficiency, follow these guidelines:\n"
    "- Write concise, efficient code that directly serves the intended purpose.\n"
    "- Avoid unnecessary operations (e.g., excessive loops, recursion, or heavy computations).\n"
    "- Handle potential errors gracefully (e.g., using try-except blocks).\n"
    "\n"
    "Return your response strictly in the following JSON format:\n"
    '{\n  "code": "<your_python_code_here>"\n}\n\n'
)


DEFAULT_FUNCTION_REFERENCE_PREFIX_PROMPT = (
    "Below functions are included in global scope and can be used in your code.\n"
    "Do not try to redefine the function(s).\n"
    "You don't have to force yourself to use these tools - use them only when you need to.\n"
)
DEFAULT_FUNCTION_REFERENCE_SEPARATOR = "\n---\n"  # Separator to distinguish different function references

PYTHON_CODE_PATTERN: re.Pattern[str] = re.compile(r"```(?:python\s*\n)?(.*?)```", re.DOTALL)


class Chatterer(BaseModel):
    """Language model for generating text from a given input."""

    client: BaseChatModel
    structured_output_kwargs: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_provider(
        cls,
        provider_and_model: str,
        structured_output_kwargs: Optional[dict[str, Any]] = {"strict": True},
    ) -> Self:
        backend, model = provider_and_model.split(":", 1)
        if backend == "openai":
            return cls.openai(model=model, structured_output_kwargs=structured_output_kwargs)
        elif backend == "anthropic":
            return cls.anthropic(model_name=model, structured_output_kwargs=structured_output_kwargs)
        elif backend == "google":
            return cls.google(model=model, structured_output_kwargs=structured_output_kwargs)
        elif backend == "ollama":
            return cls.ollama(model=model, structured_output_kwargs=structured_output_kwargs)
        elif backend == "openrouter":
            return cls.open_router(model=model, structured_output_kwargs=structured_output_kwargs)
        else:
            raise ValueError(f"Unsupported backend model: {backend}")

    @classmethod
    def openai(
        cls,
        model: str = "gpt-4o-mini",
        structured_output_kwargs: Optional[dict[str, Any]] = {"strict": True},
    ) -> Self:
        from langchain_openai import ChatOpenAI

        return cls(client=ChatOpenAI(model=model), structured_output_kwargs=structured_output_kwargs or {})

    @classmethod
    def anthropic(
        cls,
        model_name: str = "claude-3-7-sonnet-20250219",
        structured_output_kwargs: Optional[dict[str, Any]] = None,
    ) -> Self:
        from langchain_anthropic import ChatAnthropic

        return cls(
            client=ChatAnthropic(model_name=model_name, timeout=None, stop=None),
            structured_output_kwargs=structured_output_kwargs or {},
        )

    @classmethod
    def google(
        cls,
        model: str = "gemini-2.0-flash",
        structured_output_kwargs: Optional[dict[str, Any]] = None,
    ) -> Self:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return cls(
            client=ChatGoogleGenerativeAI(model=model),
            structured_output_kwargs=structured_output_kwargs or {},
        )

    @classmethod
    def ollama(
        cls,
        model: str = "deepseek-r1:1.5b",
        structured_output_kwargs: Optional[dict[str, Any]] = None,
    ) -> Self:
        from langchain_ollama import ChatOllama

        return cls(
            client=ChatOllama(model=model),
            structured_output_kwargs=structured_output_kwargs or {},
        )

    @classmethod
    def open_router(
        cls,
        model: str = "openrouter/quasar-alpha",
        structured_output_kwargs: Optional[dict[str, Any]] = None,
    ) -> Self:
        from langchain_openai import ChatOpenAI

        return cls(
            client=ChatOpenAI(
                model=model,
                base_url="https://openrouter.ai/api/v1",
                api_key=secret_from_env("OPENROUTER_API_KEY", default=None)(),
            ),
            structured_output_kwargs=structured_output_kwargs or {},
        )

    @property
    def invoke(self):
        return self.client.invoke

    @property
    def ainvoke(self):
        return self.client.ainvoke

    @property
    def stream(self):
        return self.client.stream

    @property
    def astream(self):
        return self.client.astream

    @property
    def bind_tools(self):  # pyright: ignore[reportUnknownParameterType]
        return self.client.bind_tools  # pyright: ignore[reportUnknownParameterType, reportUnknownVariableType, reportUnknownMemberType]

    def __getattr__(self, name: str) -> Any:
        return getattr(self.client, name)

    @overload
    def __call__(
        self,
        messages: LanguageModelInput,
        response_model: Type[PydanticModelT],
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> PydanticModelT: ...

    @overload
    def __call__(
        self,
        messages: LanguageModelInput,
        response_model: None = None,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str: ...

    def __call__(
        self,
        messages: LanguageModelInput,
        response_model: Optional[Type[PydanticModelT]] = None,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str | PydanticModelT:
        if response_model:
            return self.generate_pydantic(response_model, messages, config, stop, **kwargs)
        return self.client.invoke(input=messages, config=config, stop=stop, **kwargs).text()

    def generate(
        self,
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str:
        return self.client.invoke(input=messages, config=config, stop=stop, **kwargs).text()

    async def agenerate(
        self,
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str:
        return (await self.client.ainvoke(input=messages, config=config, stop=stop, **kwargs)).text()

    def generate_stream(
        self,
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        for chunk in self.client.stream(input=messages, config=config, stop=stop, **kwargs):
            yield chunk.text()

    async def agenerate_stream(
        self,
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        async for chunk in self.client.astream(input=messages, config=config, stop=stop, **kwargs):
            yield chunk.text()

    def generate_pydantic(
        self,
        response_model: Type[PydanticModelT],
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> PydanticModelT:
        result: StructuredOutputType = _with_structured_output(
            client=self.client,
            response_model=response_model,
            structured_output_kwargs=self.structured_output_kwargs,
        ).invoke(input=messages, config=config, stop=stop, **kwargs)
        if isinstance(result, response_model):
            return result
        else:
            return response_model.model_validate(result)

    async def agenerate_pydantic(
        self,
        response_model: Type[PydanticModelT],
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> PydanticModelT:
        result: StructuredOutputType = await _with_structured_output(
            client=self.client,
            response_model=response_model,
            structured_output_kwargs=self.structured_output_kwargs,
        ).ainvoke(input=messages, config=config, stop=stop, **kwargs)
        if isinstance(result, response_model):
            return result
        else:
            return response_model.model_validate(result)

    def generate_pydantic_stream(
        self,
        response_model: Type[PydanticModelT],
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Iterator[PydanticModelT]:
        try:
            import instructor
        except ImportError:
            raise ImportError("Please install `instructor` with `pip install instructor` to use this feature.")

        partial_response_model = instructor.Partial[response_model]
        for chunk in _with_structured_output(
            client=self.client,
            response_model=partial_response_model,
            structured_output_kwargs=self.structured_output_kwargs,
        ).stream(input=messages, config=config, stop=stop, **kwargs):
            yield response_model.model_validate(chunk)

    async def agenerate_pydantic_stream(
        self,
        response_model: Type[PydanticModelT],
        messages: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[PydanticModelT]:
        try:
            import instructor
        except ImportError:
            raise ImportError("Please install `instructor` with `pip install instructor` to use this feature.")

        partial_response_model = instructor.Partial[response_model]
        async for chunk in _with_structured_output(
            client=self.client,
            response_model=partial_response_model,
            structured_output_kwargs=self.structured_output_kwargs,
        ).astream(input=messages, config=config, stop=stop, **kwargs):
            yield response_model.model_validate(chunk)

    def describe_image(self, image_url: str, instruction: str = DEFAULT_IMAGE_DESCRIPTION_INSTRUCTION) -> str:
        """
        Create a detailed description of an image using the Vision Language Model.
        - image_url: Image URL to describe
        """
        return self.generate([
            HumanMessage(
                content=[{"type": "text", "text": instruction}, {"type": "image_url", "image_url": {"url": image_url}}],
            )
        ])

    async def adescribe_image(self, image_url: str, instruction: str = DEFAULT_IMAGE_DESCRIPTION_INSTRUCTION) -> str:
        """
        Create a detailed description of an image using the Vision Language Model asynchronously.
        - image_url: Image URL to describe
        """
        return await self.agenerate([
            HumanMessage(
                content=[{"type": "text", "text": instruction}, {"type": "image_url", "image_url": {"url": image_url}}],
            )
        ])

    def get_approximate_token_count(self, message: BaseMessage) -> int:
        return self.client.get_num_tokens_from_messages([message])  # pyright: ignore[reportUnknownMemberType]

    def get_usage_metadata(self, message: BaseMessage) -> UsageMetadata:
        if isinstance(message, AIMessage):
            usage_metadata = message.usage_metadata
            if usage_metadata is not None:
                input_tokens = usage_metadata["input_tokens"]
                output_tokens = usage_metadata["output_tokens"]
                return {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }
            else:
                approx_tokens = self.get_approximate_token_count(message)
                return {"input_tokens": 0, "output_tokens": approx_tokens, "total_tokens": approx_tokens}
        else:
            approx_tokens = self.get_approximate_token_count(message)
            return {
                "input_tokens": approx_tokens,
                "output_tokens": 0,
                "total_tokens": approx_tokens,
            }

    def invoke_code_execution(
        self,
        messages: LanguageModelInput,
        repl_tool: Optional["PythonAstREPLTool"] = None,
        prompt_for_code_invoke: Optional[str] = DEFAULT_CODE_GENERATION_PROMPT,
        function_signatures: Optional[FunctionSignature | Iterable[FunctionSignature]] = None,
        function_reference_prefix: Optional[str] = DEFAULT_FUNCTION_REFERENCE_PREFIX_PROMPT,
        function_reference_seperator: str = DEFAULT_FUNCTION_REFERENCE_SEPARATOR,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> CodeExecutionResult:
        if not function_signatures:
            function_signatures = []
        elif isinstance(function_signatures, FunctionSignature):
            function_signatures = [function_signatures]
        messages = augment_prompt_for_toolcall(
            function_signatures=function_signatures,
            messages=messages,
            prompt_for_code_invoke=prompt_for_code_invoke,
            function_reference_prefix=function_reference_prefix,
            function_reference_seperator=function_reference_seperator,
        )
        code_obj: PythonCodeToExecute = self.generate_pydantic(
            response_model=PythonCodeToExecute, messages=messages, config=config, stop=stop, **kwargs
        )
        return CodeExecutionResult.from_code(
            code=code_obj.code,
            config=config,
            repl_tool=repl_tool,
            function_signatures=function_signatures,
            **kwargs,
        )

    async def ainvoke_code_execution(
        self,
        messages: LanguageModelInput,
        repl_tool: Optional["PythonAstREPLTool"] = None,
        prompt_for_code_invoke: Optional[str] = DEFAULT_CODE_GENERATION_PROMPT,
        additional_callables: Optional[Callable[..., object] | Sequence[Callable[..., object]]] = None,
        function_reference_prefix: Optional[str] = DEFAULT_FUNCTION_REFERENCE_PREFIX_PROMPT,
        function_reference_seperator: str = DEFAULT_FUNCTION_REFERENCE_SEPARATOR,
        config: Optional[RunnableConfig] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> CodeExecutionResult:
        function_signatures: list[FunctionSignature] = FunctionSignature.from_callable(additional_callables)
        messages = augment_prompt_for_toolcall(
            function_signatures=function_signatures,
            messages=messages,
            prompt_for_code_invoke=prompt_for_code_invoke,
            function_reference_prefix=function_reference_prefix,
            function_reference_seperator=function_reference_seperator,
        )
        code_obj: PythonCodeToExecute = await self.agenerate_pydantic(
            response_model=PythonCodeToExecute, messages=messages, config=config, stop=stop, **kwargs
        )
        return await CodeExecutionResult.afrom_code(
            code=code_obj.code,
            config=config,
            repl_tool=repl_tool,
            function_signatures=function_signatures,
            **kwargs,
        )


class PythonCodeToExecute(BaseModel):
    code: str = Field(description="Python code to execute")

    def model_post_init(self, context: object) -> None:
        super().model_post_init(context)

        codes: list[str] = []
        for match in PYTHON_CODE_PATTERN.finditer(self.code):
            codes.append(match.group(1))
        if codes:
            self.code = "\n".join(codes)


def _with_structured_output(
    client: BaseChatModel,
    response_model: Type["PydanticModelT | Partial[PydanticModelT]"],
    structured_output_kwargs: dict[str, Any],
) -> Runnable[LanguageModelInput, dict[object, object] | BaseModel]:
    return client.with_structured_output(schema=response_model, **structured_output_kwargs)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
