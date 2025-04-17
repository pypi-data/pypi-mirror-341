class MemoryAPI:
    def __init__(self, client):
        self.client = client

    async def store(self, namespace: str, content: str):
        async with self.client.get_session() as session:
            async with session.post(
                f"{self.client.base_url}/memory/store",
                json={"namespace": namespace, "content": content}
            ) as resp:
                return await resp.json()

    async def search(self, namespace: str, query: str, top_k: int = 5):
        async with self.client.get_session() as session:
            async with session.post(
                f"{self.client.base_url}/memory/search",
                json={"namespace": namespace, "query": query, "top_k": top_k}
            ) as resp:
                return await resp.json()