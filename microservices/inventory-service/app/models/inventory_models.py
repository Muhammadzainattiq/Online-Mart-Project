from sqlmodel import SQLModel, Field
from datetime import datetime
   

class InventoryItemCreate(SQLModel):
    product_id: int
    product_name: str
    color_id: int
    size_id: int
    stock_quantity: int = Field(default=0)
    last_updated: datetime = Field(default=datetime.now)


class InventoryItem(InventoryItemCreate, table=True):
    inventory_item_id: int | None = Field(default=None, primary_key=True)


