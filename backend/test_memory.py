from app.memory.session_manager import session_manager

memory = session_manager.get_session("abc123")

memory.add_user_message("Plan a Goa trip")

memory.add_assistant_message("Sure! What's your budget?")

memory.add_user_message("₹30000")

print(memory.get_history())