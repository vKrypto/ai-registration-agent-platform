from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/ready")
def ready() -> dict[str, str]:
    # TODO: Add database, storage, and Key Vault readiness checks.
    return {"status": "ready"}
