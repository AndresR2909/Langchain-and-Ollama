from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_core.output_parsers import StrOutputParser

load_dotenv("./../.env")


class ChatBot:
    """
    Chatbot class to interact with the LLM model.
    Args:
    base_url (str): The base url of the LLM model.
    model (str): The model name.
    rol_template (str): The role template for the chatbot.
    """

    def __init__(self, base_url, model, rol_template="You are helpful assistant."):
        self.base_url = base_url
        self.model = model
        self.llm = ChatOllama(base_url=base_url, model=model)
        self._setup_chatbot(rol_template)

    def _setup_chatbot(self, new_rol_template):
        self.rol_template = new_rol_template
        system = SystemMessagePromptTemplate.from_template(self.rol_template)
        human = HumanMessagePromptTemplate.from_template("{input}")

        messages = [system, MessagesPlaceholder(variable_name="history"), human]

        self.prompt = ChatPromptTemplate(messages=messages)

        self.chain = self.prompt | self.llm | StrOutputParser()

        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def chat(self, session_id, input):
        for output in self.runnable_with_history.stream(
            {"input": input}, config={"configurable": {"session_id": session_id}}
        ):
            yield output

    @staticmethod
    def get_session_history(session_id):
        return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")
