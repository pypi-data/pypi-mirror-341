class APIError(Exception):
    def __init__(self, detail: str):
        super().__init__(f"Error: {detail}")
        self.detail = detail

    def __str__(self):
        return f"APIError: - {self.detail}"
