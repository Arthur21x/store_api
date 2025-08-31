from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException
from fastapi import HTTPException

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

@router.post("/products")
async def create_product(product: ProductSchema):
    try:
        return await save_product(product)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Produto já cadastrado.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro inesperado ao criar produto.")


@router.get("/products")
async def list_products(
    price_min: float = Query(None),
    price_max: float = Query(None)
):
    products = await get_products_filtered(price_min=price_min, price_max=price_max)
    return products


@router.get("/products")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    order_by: str = Query("name")
):
    products = await get_products_filtered(skip=skip, limit=limit, order_by=order_by)
    return products

