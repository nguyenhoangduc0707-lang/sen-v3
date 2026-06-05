class EchoWorker:
    def run(self, **kwargs):
        return {"status": "ok", "summary": f"Echo: {kwargs}"}
