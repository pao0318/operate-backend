from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse

router = APIRouter()


@router.get("/{case_id}/documents")
async def get_documents(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.case_id == case_id)
    )
    documents = result.scalars().all()
    
    return {
        "data": {
            "documents": [
                DocumentResponse.from_orm(d).dict()
                for d in documents
            ]
        }
    }
