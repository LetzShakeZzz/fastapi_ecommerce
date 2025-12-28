from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy import select

from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel


async def update_product_rating(product_id: int, db: AsyncSession):
    """
    Пересчитывает и обновляет рейтинг продукта
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active
        )
    )
    avg_rating = result.scalar() or 0.0
    
    product = await db.get(ProductModel, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    product.rating = avg_rating

    await db.commit()
    await db.refresh(product)