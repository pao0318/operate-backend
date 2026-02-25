import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque


class SSEManager:
    def __init__(self, max_events_cache: int = 10):
        self._clients: Dict[str, asyncio.Queue] = {}
        self._recent_events: deque = deque(maxlen=max_events_cache)
    
    async def connect(self, client_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self._clients[client_id] = queue
        
        connection_event = {
            "type": "connection",
            "clientId": client_id
        }
        await queue.put(json.dumps(connection_event))
        
        if self._recent_events:
            history_event = {
                "type": "history",
                "events": list(self._recent_events)
            }
            await queue.put(json.dumps(history_event))
        
        return queue
    
    def disconnect(self, client_id: str) -> None:
        if client_id in self._clients:
            del self._clients[client_id]
    
    async def broadcast(self, event: Dict[str, Any]) -> None:
        self._recent_events.append(event)
        
        event_str = json.dumps(event)
        for client_id, queue in list(self._clients.items()):
            try:
                await queue.put(event_str)
            except Exception:
                self.disconnect(client_id)
    
    def create_navigation_event(
        self,
        action: str,
        target_app_id: str,
        route: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return {
            "id": str(uuid.uuid4()),
            "type": "navigation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "targetAppId": target_app_id,
            "route": route,
            "data": data
        }
    
    @property
    def client_count(self) -> int:
        return len(self._clients)


sse_manager = SSEManager()
