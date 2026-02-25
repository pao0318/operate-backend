from fastapi import APIRouter
from app.api.endpoints import (
    health,
    sse,
    available_services,
    cases,
    documents,
    extracted_key_metrics,
    covenant_status,
    quarterly_dscr,
    quarter_financial_drivers,
    q3_highlights,
    fry14_schedule_template,
    detailed_findings_y14,
    shipment_details,
    operational_findings,
    datasimulator_benefits,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sse.router, tags=["SSE"])
api_router.include_router(available_services.router, prefix="/available-services", tags=["Available Services"])
api_router.include_router(cases.router, prefix="/case", tags=["Cases"])
api_router.include_router(documents.router, prefix="/case", tags=["Documents"])
api_router.include_router(extracted_key_metrics.router, prefix="/case", tags=["Extracted Key Metrics"])
api_router.include_router(covenant_status.router, prefix="/case", tags=["Covenant Status"])
api_router.include_router(quarterly_dscr.router, prefix="/case", tags=["Quarterly DSCR"])
api_router.include_router(quarter_financial_drivers.router, prefix="/case", tags=["Quarter Financial Drivers"])
api_router.include_router(q3_highlights.router, prefix="/case", tags=["Q3 Highlights"])
api_router.include_router(fry14_schedule_template.router, prefix="/case", tags=["FR Y14 Schedule Template"])
api_router.include_router(detailed_findings_y14.router, prefix="/case", tags=["Detailed Findings Y14"])
api_router.include_router(shipment_details.router, prefix="/case", tags=["Shipment Details"])
api_router.include_router(operational_findings.router, prefix="/case", tags=["Operational Findings"])
api_router.include_router(datasimulator_benefits.router, prefix="/case", tags=["Datasimulator Benefits"])
