import os
from tiptree import Agent, CustomProviderConfig

os.environ["TIPTREE_API_KEY"] = "tiptree-yKhhVSf6Y5MkIOL0KBII9zsPLZZMVSe2Uy_qKp5kurE"
os.environ["TIPTREE_API_BASE"] = "https://dev.api.tiptreesystems.com/platform"

agent = Agent.get_or_create(name="Don")
# prompt = input("c(ontinue) / q(uit)")
# if prompt == "q":
#     exit()

# custom_provider_config = CustomProviderConfig(
#     name="nasim-local",
#     base_url="https://present-skylark-simply.ngrok-free.app/provider",
#     api_key="secret-api-key",
# )

# agent = agent.update(custom_provider_configs=[])
agent = agent.add_custom_provider(
    name="nasim-local",
    base_url="https://present-skylark-simply.ngrok-free.app",
    api_key="secret-api-key",
)
print(agent)

session = agent.create_agent_session()

session.send_message("Please send me an SMS with a test message.")
#
# response = session.wait_for_next_message()
# print(response.content)