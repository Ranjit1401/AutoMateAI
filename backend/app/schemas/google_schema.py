from typing import List, Optional

from pydantic import BaseModel, Field


class SendEmailRequest(BaseModel):

    to: str = Field(description="Recipient email address")

    subject: str = Field(description="Email subject line")

    body: str = Field(description="Plain text (or HTML) email body")

    cc: Optional[List[str]] = Field(default=None)

    bcc: Optional[List[str]] = Field(default=None)

    is_html: bool = Field(default=False, description="Set true if `body` is HTML")



class CreateCalendarEventRequest(BaseModel):

    summary: str = Field(description="Event title")

    description: Optional[str] = Field(default=None)

    start_time: str = Field(description="ISO 8601 start datetime, e.g. 2026-08-01T10:00:00")

    end_time: str = Field(description="ISO 8601 end datetime, e.g. 2026-08-01T10:30:00")

    timezone: str = Field(default="UTC")

    attendees: Optional[List[str]] = Field(default=None, description="List of attendee emails")

    location: Optional[str] = Field(default=None)



class UploadFileRequest(BaseModel):

    file_name: str = Field(description="Name to store the file as in Drive")

    file_content_base64: str = Field(description="Base64 encoded file content")

    mime_type: str = Field(default="application/octet-stream")

    folder_id: Optional[str] = Field(default=None, description="Target Drive folder id")



class AppendSheetRowRequest(BaseModel):

    spreadsheet_id: str = Field(description="Target Google Sheet id")

    range_name: str = Field(default="Sheet1!A1", description="A1 notation range to append after")

    values: List[str] = Field(description="Row values to append, in column order")

