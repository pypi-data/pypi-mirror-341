from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobInboxConversation import JobInboxConversation

class JobInboxGetResponse(BaseModel):
    conversations: list[JobInboxConversation]
