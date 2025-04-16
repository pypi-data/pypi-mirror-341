import os
from fastapi import APIRouter, HTTPException
import aiohttp
from urllib.parse import urljoin
import json

router = APIRouter()

router = APIRouter(prefix="/botrun_back")


def normalize_url(base_url, path):
    f_base_url = base_url
    if not f_base_url.endswith("/"):
        f_base_url = f_base_url + "/"
    return urljoin(f_base_url, path)


@router.get("/info")
async def get_botrun_back_info():
    """Get information from the botrun backend service."""
    try:
        botrun_base_url = os.environ.get("BOTRUN_BACK_API_BASE")
        if not botrun_base_url:
            raise HTTPException(
                status_code=500, detail="BOTRUN_BACK_API_BASE not configured"
            )

        info_url = normalize_url(botrun_base_url, "botrun/info")

        async with aiohttp.ClientSession() as session:
            async with session.get(info_url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error calling botrun backend: {error_text}",
                    )

                text = await response.text()
                return json.loads(text)
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to botrun backend: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
