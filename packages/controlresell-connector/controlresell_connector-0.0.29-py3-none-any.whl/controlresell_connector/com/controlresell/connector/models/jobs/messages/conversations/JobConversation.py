from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.JobConversationOppositeUser import JobConversationOppositeUser
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationTransaction import JobConversationTransaction
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessage import JobConversationMessage

class JobConversation(BaseModel):
    id: str
    readByCurrentUser: Optional[bool] = None
    readByOppositeUser: Optional[bool] = None
    allowReply: Optional[bool] = None
    isSuspicious: Optional[bool] = None
    isDeletionRestricted: Optional[bool] = None
    userHasSupportRole: Optional[bool] = None
    oppositeUser: Optional[JobConversationOppositeUser] = None
    transaction: Optional[JobConversationTransaction] = None
    messages: list[JobConversationMessage]
