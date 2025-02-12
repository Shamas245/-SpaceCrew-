# test_memory.py
from agent.memory.conversation_manager import ConversationManager

def test_memory():
    print("Testing Conversation Manager...")
    manager = ConversationManager()
    
    # Test adding and retrieving memories
    test_conversations = [
        ("Who is in space?", "There are 7 astronauts currently in space."),
        ("What do they do?", "They conduct various scientific experiments."),
    ]
    
    print("\nTesting memory storage...")
    for query, response in test_conversations:
        try:
            manager.add_to_memory(query, response)
            print(f"✓ Successfully added to memory: {query}")
        except Exception as e:
            print(f"✗ Failed to add to memory: {str(e)}")
    
    print("\nTesting memory retrieval...")
    try:
        context = manager.get_context()
        print("✓ Successfully retrieved context!")
        print(f"Context: {context}")
    except Exception as e:
        print(f"✗ Failed to retrieve context: {str(e)}")

if __name__ == "__main__":
    test_memory()