from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class ColorCreate(SQLModel):
    color_name: str

class SizeCreate(SQLModel):
    size_name: str


class ProductBase(SQLModel):
    product_name: str | None = None
    product_description: str | None = None
    product_price: float | None = None
    product_image_url: str | None = None

class ProductCreate(ProductBase):
    product_category_ids: List[int] = []
    colors: List[ColorCreate]
    sizes: List[SizeCreate]

class ProductCategory(SQLModel, table=True):
    product_id: int = Field(default=None, foreign_key="product.product_id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="category.category_id", primary_key=True)

class Product(ProductBase, table=True):
    product_id: int | None= Field(default=None, primary_key=True)

    colors: List["ProductColor"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    sizes: List["ProductSize"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    categories: list["Category"] = Relationship(
        back_populates="products",
        link_model=ProductCategory
    )


class ProductUpdate(ProductBase):
    pass

class CategoryBase(SQLModel):
    category_name: str
    category_description: None | str = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    category_id:int

class Category(CategoryBase, table=True):
    category_id: int | None = Field(default=None, primary_key=True)
    products: list[Product] = Relationship(
        back_populates="categories",
        link_model=ProductCategory
    )



class CategoryUpdate(CategoryBase):
    pass

class Color(SQLModel, table=True):
    color_id: int | None = Field(default=None, primary_key=True)
    color_name: str

class Size(SQLModel, table=True):
    size_id: int | None = Field(default=None, primary_key=True)
    size_name: str

class ProductColor(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True, foreign_key="product.product_id")
    color_id: int = Field(default=None, primary_key=True, foreign_key="color.color_id")
    product: Product = Relationship(back_populates="colors")
    color: Color = Relationship()

class ProductSize(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True, foreign_key="product.product_id")
    size_id: int = Field(default=None, primary_key=True, foreign_key="size.size_id")
    product: Product = Relationship(back_populates="sizes")
    size: Size = Relationship()
