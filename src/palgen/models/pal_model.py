from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class Pal(BaseModel):
    """Model for Pal data."""
    model_config = ConfigDict(extra="ignore")

    bp_class: str = Field(..., alias="BPClass") # Blueprint class of the Pal (e.g. LizardMan).
                                                # Can be used as a unique identifier for the Pal.
    text_name: Optional[str] = "" # Actual name of the Pal based on localization (e.g. BlueberryFairy = Prunelia).

    tribe: str = Field(..., alias="Tribe") # Tribe of the Pal (e.g. EPalTribeID::LizardMan_Fire).
    genus: str = Field(..., alias="GenusCategory") # Genus of the Pal (e.g. EPalGenusType::Humanoid).

    """Index"""
    internal_index: int # Unique index of the Pal in the game data.
    zukan_index: int = Field(..., alias="ZukanIndex") # Unique index for the Pal in the Zukan (Palpedia).
    variant: str = Field(..., alias="ZukanIndexSuffix") # Variant suffix for the Pal in the Zukan (#153B, #153C, etc.).

    """Egg and Size Information"""
    size: str = Field(..., alias="Size") # Size of the Pal (e.g. EPalSizeType::S).
    rarity: int = Field(..., alias="Rarity") # Rarity of the Pal for the egg size (e.g. 3, 6).

    """Elements"""
    element1: str = Field(..., alias="ElementType1") # Primary element of the Pal (e.g. EPalElementType::Fire).
    element2: str = Field(..., alias="ElementType2") # Secondary element of the Pal (e.g. EPalElementType::Water).

    """Breeding Information"""
    combirank: int = Field(..., alias="CombiRank") # Rank of the Pal in breeding combinations
                                                   # (Used for determining breeding outcomes).

    """Work Suitability"""
    kindling: int = Field(..., alias="WorkSuitability_EmitFlame")
    watering: int = Field(..., alias="WorkSuitability_Watering")
    planting: int = Field(..., alias="WorkSuitability_Seeding")
    electricity: int = Field(..., alias="WorkSuitability_GenerateElectricity")
    handiwork: int = Field(..., alias="WorkSuitability_Handcraft")
    gathering: int = Field(..., alias="WorkSuitability_Collection")
    lumbering: int = Field(..., alias="WorkSuitability_Deforest")
    mining: int = Field(..., alias="WorkSuitability_Mining")
    oil_extract: int = Field(..., alias="WorkSuitability_OilExtraction")
    medicine: int = Field(..., alias="WorkSuitability_ProductMedicine")
    cooling: int = Field(..., alias="WorkSuitability_Cool")
    transport: int = Field(..., alias="WorkSuitability_Transport")
    ranching: int = Field(..., alias="WorkSuitability_MonsterFarm")

class PalTable(Base):
    """SQLAlchemy table for Pal data."""
    __tablename__ = 'pals'

    internal_index: Mapped[int] = mapped_column(primary_key=True)
    bp_class: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    text_name: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)
    tribe: Mapped[str] = mapped_column(sa.String, nullable=False)
    genus: Mapped[str] = mapped_column(sa.String, nullable=False)

    """Index"""
    zukan_index: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    variant: Mapped[str] = mapped_column(sa.String, nullable=True)

    """Egg and Size Information"""
    size: Mapped[str] = mapped_column(sa.String, nullable=False)
    rarity: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    """Elements"""
    element1: Mapped[str] = mapped_column(sa.String, nullable=True)
    element2: Mapped[str] = mapped_column(sa.String, nullable=True)

    """Breeding Information"""
    combirank: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    """Work Suitability"""
    kindling: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    watering: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    planting: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    electricity: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    handiwork: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    gathering: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    lumbering: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    mining: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    oil_extract: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    medicine: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    cooling: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    transport: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    ranching: Mapped[int] = mapped_column(sa.Integer, nullable=False)