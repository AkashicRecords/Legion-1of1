class ComputerVisionAgent:
    async def handle_task(self, task):
        data = task['data']
        print(f"Processing image data: {data}")
        # Add computer vision logic here