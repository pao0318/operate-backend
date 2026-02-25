import uuid
import asyncio
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.sse_manager import sse_manager
from app.schemas.sse import NavigationRequest

router = APIRouter()


async def event_generator(client_id: str, request: Request):
    queue = await sse_manager.connect(client_id)
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                data = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield f"data: {data}\n\n"
            except asyncio.TimeoutError:
                yield f"data: {{}}\n\n"
    finally:
        sse_manager.disconnect(client_id)


@router.get("/sse")
async def sse_endpoint(request: Request):
    client_id = str(uuid.uuid4())
    return StreamingResponse(
        event_generator(client_id, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )


@router.post("/navigation")
async def publish_navigation(nav_request: NavigationRequest):
    event = sse_manager.create_navigation_event(
        action=nav_request.action,
        target_app_id=nav_request.target_app_id,
        route=nav_request.route,
        data=nav_request.data
    )
    
    await sse_manager.broadcast(event)
    
    return {"success": True, "event": event}


@router.get("/sse/health")
async def sse_health():
    return {
        "status": "ok",
        "clients": sse_manager.client_count,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
