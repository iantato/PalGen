import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict, model_validator
from palgen.models.base import Base

class CombiUniqueModel(BaseModel):
    """Model for Combi Unique data."""
    model_config = ConfigDict(extra="ignore")

    parents: list[dict[str, str]] = Field(default_factory=list)
    child_id: str = Field(..., alias="ChildCharacterID")  # Unique identifier (Blueprint) for the child Pal (e.g. Baphomet_Dark).

    @model_validator(mode='before')
    @classmethod
    def combine_parent_data(cls, data):
        if isinstance(data, dict):
            parent_a = {
                'tribe': data.get('ParentTribeA', ''),
                'gender': data.get('ParentGenderA', '')
            }
            parent_b = {
                'tribe': data.get('ParentTribeB', ''),
                'gender': data.get('ParentGenderB', '')
            }

            data['parents'] = [parent_a, parent_b]

        return data

class CombiUniqueTable(Base):
    """SQLAlchemy table for Combi Unique data."""
    __tablename__ = 'combi_unique'

    parents: Mapped[list[dict[str, str]]] = mapped_column(sa.JSON, nullable=False)
    child_id: Mapped[str] = mapped_column(sa.String, primary_key=True, nullable=False)