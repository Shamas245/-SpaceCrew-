from langchain.memory import ConversationBufferMemory
class ConversationManager:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
    
    def add_to_memory(self, query: str, response: str):
        self.memory.save_context(
            {"input": query},
            {"output": response}
        )
    
    def get_context(self) -> str:
        return self.memory.load_memory_variables({})["chat_history"]