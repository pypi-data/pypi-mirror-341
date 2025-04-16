from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class MailEvent(BaseModel):
    client_ip: str = Field(alias="clientIp")
    date: str  # ISO формат даты
    event_type: Literal[
        'mailbox_send',
        'message_receive',
        'message_seen',
        'message_unseen',
        'message_forward',
        'message_purge',
        'message_trash',
        'message_spam',
        'message_unspam',
        'message_move',
        'message_copy',
        'message_answer'
        ] = Field(alias='eventType')
    org_id: int = Field(alias="orgId")
    request_id: str = Field(alias="requestId")
    source: str
    uniq_id: str = Field(alias="uniqId")
    user_login: str = Field(alias="userLogin")
    user_name: str = Field(alias="userName")
    user_uid: str = Field(alias="userUid")
    actor_uid: Optional[str] = Field(alias="actorUid", default=None)
    bcc: Optional[str] = None
    cc: Optional[str] = None
    to: Optional[str] = None
    dest_mid: Optional[str] = Field(alias="destMid", default=None)
    folder_name: Optional[str] = Field(alias="folderName", default=None)
    folder_type: Optional[
        Literal[
            'inbox',
            'sent',
            'trash',
            'spam',
            'drafts',
            'outbox',
            'archive',
            'template_',
            'discount',
            'restored',
            'reply_later',
            'user'
            ]
        ] = Field(alias="folderType", default=None)
    from_s: Optional[str] = Field(alias="from", default=None)
    labels: Optional[List[str]] = None
    mid: Optional[str] = None
    msg_id: Optional[str] = Field(alias="msgId", default=None)


class MailEventsPage(BaseModel):
    events: List[MailEvent]
    nextPageToken: Optional[str] = ''


