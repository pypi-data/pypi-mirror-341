from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessageType import JobConversationMessageType
from datetime import datetime

class JobConversationMessage(BaseModel):
    id: str
    body: Optional[str] = None
    photos: Optional[list[str]] = None
    userId: str
    isHidden: Optional[bool] = None
    type: JobConversationMessageType
    createdAt: datetime
