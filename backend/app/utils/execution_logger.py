def log_step(state, agent, message, status="completed"):
    state.setdefault("execution_log", []).append({
        "agent": agent,
        "status": status,
        "message": message,
    })