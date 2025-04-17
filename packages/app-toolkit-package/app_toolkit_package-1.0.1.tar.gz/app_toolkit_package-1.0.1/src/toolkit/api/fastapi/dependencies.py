from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import cache_config, db_config
from .utils import get_client_info, set_headers_no_client_cache

# HTTP dependencies
client_info = Annotated[dict[str, Any], Depends(get_client_info)]
set_headers = Depends(set_headers_no_client_cache)

# Repos dependencies
redis = Annotated[cache_config.aioredis.Redis, Depends(cache_config.get_aioredis)]
async_session = Annotated[AsyncSession, Depends(db_config.get_async_session)]
