from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:

        if body["messages"]:
            body["messages"] = [body["messages"][-1]]

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:

        return body
