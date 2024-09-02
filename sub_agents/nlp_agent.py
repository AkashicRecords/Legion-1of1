class NLPAagent:
    async def handle_task(self, task):
        data = task['data']
        print(f"Processing text data: {data}")
        # Add NLP logic here