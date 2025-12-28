from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db_depends import get_async_db
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.service.rating import update_product_rating

from app.auth import get_current_buyer


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active))
    return result.all()


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer)
):
    """
    Создаёт новый отзыв.
    """
    # Проверяем, существует ли активный товар
    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active)
    )
    product = product_result.first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Создание нового отзыва
    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)

    #Обновление рейтинга продукта
    await update_product_rating(review.product_id, db)

    return db_review


@router.delete("/{review_id}", response_model=dict)
async def update_product(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer)
):
    """
    Выполняет мягкое удаление отзыва, если он принадлежит текущему пользователю (только для 'buyer').
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id, ProductModel.is_active))
    review = result.first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive")
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own reviews")
    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(review)

    #Обновление рейтинга продукта
    await update_product_rating(review.product_id, db)

    return {"message": "Review deleted"}
