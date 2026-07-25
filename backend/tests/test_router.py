from app.agents.router_agent import RouterAgent

router = RouterAgent()

result = router.route(
    "Reply to this email professionally."
)

print(result)