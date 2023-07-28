class target:
    def __init__(self, json):
        self.json = json
        if json.get("data"):
            self.json = json.get("data")
        self.type: str = self.json[0].get("type")
        self.blogger_id: str = self.json[0].get("bloggerUrl")
        self.created_at: int = self.json[0].get("createdAt")
        self.currentSum: int = self.json[0].get("currentSum")
        self.targetSum: int = self.json[0].get("targetSum")
        self.description: str = self.json[0].get("description")

            