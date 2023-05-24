"""

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
from fastapi import FastAPI
from router import northRouter
from utils import create_logger

logger = create_logger("NFVCL-5Tonic Interface")

app = FastAPI(
    title="NFVCL-5Tonic Interface",
    version="0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(northRouter)