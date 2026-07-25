from app.memory.conversation_memory import ConversationMemory


class SessionManager:

    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str):

        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationMemory(session_id)

        return self.sessions[session_id]

    def delete_session(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]


session_manager = SessionManager() 