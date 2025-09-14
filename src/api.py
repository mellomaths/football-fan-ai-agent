from fastapi import APIRouter

from controllers.matches_controller import router as matches_api

router = APIRouter(redirect_slashes=False)

router.include_router(matches_api)
