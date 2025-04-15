from igbot_base.agent import Agent
from igbot_base.llm import Llm
from igbot_base.llmmemory import LlmMemory
from igbot_base.prompt_template import Prompt
from igbot_base.retriever import Retriever
from igbot_base.tool import Tool


class IgBotBaseException(Exception):

    def __init__(self, message, cause: Exception = None):
        super().__init__(message)
        self.cause = cause

    def __str__(self):
        result = self.args[0]
        if self.cause:
            result += f" Caused by: {self.cause}"

        return result


class BaseAgentException(IgBotBaseException):

    def __init__(self, message, agent: Agent, cause: Exception = None):
        super().__init__(message, cause)
        self.agent = agent

    def __str__(self):
        result = super().__str__()
        result += f" at agent {self.agent}"


class BaseLlmException(IgBotBaseException):

    def __init__(self, message, llm: Llm, cause: Exception = None):
        super().__init__(message, cause)
        self.llm = llm

    def __str__(self):
        result = super().__str__()
        result += f" at llm {self.llm}"


class BaseMemoryException(IgBotBaseException):

    def __init__(self, message, memory: LlmMemory, cause: Exception = None):
        super().__init__(message, cause)
        self.memory = memory

    def __str__(self):
        result = super().__str__()
        result += f" at memory {self.memory}"


class BasePromptException(IgBotBaseException):

    def __init__(self, message, prompt: Prompt, cause: Exception = None):
        super().__init__(message, cause)
        self.prompt = prompt

    def __str__(self):
        result = super().__str__()
        result += f" at prompt {self.prompt}"


class BaseRetrieverException(IgBotBaseException):

    def __init__(self, message, retriever: Retriever, cause: Exception = None):
        super().__init__(message, cause)
        self.retriever = retriever

    def __str__(self):
        result = super().__str__()
        result += f" at retriever {self.retriever}"


class BaseToolException(IgBotBaseException):

    def __init__(self, message, tool: Tool, cause: Exception = None):
        super().__init__(message, cause)
        self.tool = tool

    def __str__(self):
        result = super().__str__()
        result += f" at tool {self.tool}"
