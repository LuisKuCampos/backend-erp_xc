import os
from fastapi import Request, HTTPException, Query
from typing import Dict, Any

API_KEY = os.environ.get("API_KEY", "12345")

def verify_api_key(api_key: str = Query(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

def parse_filter_query(request: Request) -> Dict[str, Any]:
    filters = {}
    for key, value in request.query_params.items():
        if key.startswith("filterQuery[") and key.endswith("]"):
            clean_key = key[12:-1]
            filters[clean_key] = value
    return filters