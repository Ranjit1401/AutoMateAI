from app.tools.executor import tool_executor

result = tool_executor.execute(

    tool_name="weather",

    city="Mumbai",

)

print(result)