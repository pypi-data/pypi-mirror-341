from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobConversationInboxOppositeUser import JobConversationInboxOppositeUser

class JobInboxConversation(BaseModel):
    id: str
    isDeletionRestricted: Optional[bool] = None
    unread: Optional[bool] = None
    updatedAt: datetime
    oppositeUser: Optional[JobConversationInboxOppositeUser] = None
