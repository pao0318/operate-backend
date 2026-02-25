from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime


class NavigationRequest(BaseModel):
    action: str
    target_app_id: str
    route: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class NavigationEvent(BaseModel):
    id: str
    type: str = "navigation"
    timestamp: str
    action: str
    target_app_id: str
    route: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class SSEHealthResponse(BaseModel):
    status: str
    clients: int
    timestamp: str


class ConnectionEvent(BaseModel):
    type: str = "connection"
    client_id: str


class HistoryEvent(BaseModel):
    type: str = "history"
    events: List[NavigationEvent]
