"""FetchUser Repository."""
from typing import Any, Dict
from abstractions.repository import IRepository

class FetchUserRepository(IRepository):
    def create_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"id": "1", **data}
