from fastapi_pagination import Page

from jarvismode.helpers.base_model import BaseModel
from jarvismode.services.database.models.flow.model import Flow
from jarvismode.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[Flow]
