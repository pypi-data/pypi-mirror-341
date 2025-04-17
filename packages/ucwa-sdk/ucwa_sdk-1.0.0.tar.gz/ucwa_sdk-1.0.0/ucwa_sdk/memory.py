class ModelAPI:
    def __init__(self, client):
        self.client = client

    async def replay(self, chat_id: str):
        async with self.client.get_session() as session:
            async with session.get(f"{self.client.base_url}/model/replay/{chat_id}") as resp:
                async for line in resp.content:
                    yield line.decode("utf-8")
