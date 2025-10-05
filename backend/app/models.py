from pydantic import BaseModel
from typing import List, Optional

class Dataset(BaseModel):
    id: str
    title: str
    domain: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    data_url: Optional[str] = None
    data_type: Optional[str] = None
    release_date: Optional[str] = None
    authors: Optional[List[str]] = None
    variables: Optional[List[str]] = None


