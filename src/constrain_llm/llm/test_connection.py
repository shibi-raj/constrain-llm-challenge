from constrain_llm.llm.factory import create_llm

llm = create_llm(
    provider="openrouter",
    model="openai/gpt-oss-120b:exacto",
    # model="openai/gpt-oss-120b:free",
    # model="openai/gpt-oss-20b:free",
    
)

response = llm.invoke("Respond with exactly: connection successful")

print(response.content)
