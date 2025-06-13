from typing import List, Dict, Union, Optional, Annotated
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator, BeforeValidator, EmailStr


class Country(BaseModel):
    name: Annotated[str, Field(..., min_length=2, description="Назва країни")]
    code: Annotated[int, Field(380, description="Код країни")]


class City(BaseModel):
    name: Annotated[str, Field(..., min_length=2, description="Назва міста")]
    country: Country


class Address(BaseModel):
    street: Annotated[str, Field(..., min_length=2, description="Назва вулиці")]
    number: Annotated[int, Field(1, gt=0, description="Номер будинку")]
    city: City

   # @model_validator(mode="after")
   # def all_fields_validate(cls, value):
   #     if len(value) < 2:
   #        raise ValueError("Мінімальна кількість символів: 2")
   #    return value


class Product(BaseModel):
    name: Annotated[str, Field(..., min_length=2)]
    quantity: Annotated[int, Field(default=1, description="Кількість товарів", gt=0)]
    date_time: Annotated[datetime, Field(default_factory=datetime.now, description="Дата завозу товару")]


def validate_full_name(value: str):
    if len(value.split()) > 2:
        raise ValueError("full_name повинен містити лише ім'я та прізвище")
    return value


class User(BaseModel):
    full_name: Annotated[str, BeforeValidator(validate_full_name)]
    products: List[Product] = Field(default=[], examples=[[dict(name="Хліб"), dict(name="Кава")]])
    address: Address
    email: EmailStr


class Order(User):
    order: List[Product] = Field(default=list, examples=[[dict(name="Хліб"), dict(name="Кава")]])

    @field_validator("full_name", mode="before")
    def validate_full_name_field(cls, value: str):
        if len(value.split()) < 2:
            raise ValueError("full_name повинен містити прізвище та ім'я")
        return value


#class Config:
#    str_min_lenght = 2
#    str_max_lenght = 200

class Config:
    json_schema_extra = {
        "full_name": "Вася Пупкін",
        "products": [
            {"name": "Кава"},
            {"name": "Цукор", "quantity": 5}
        ],
        "address": {
            "street": "Перемоги",
            "number": 67,
            "city": {
                "name": "Одеса",
                "country": {
                    "name": "Україна",
                    "code": 380
                }
            }
        },
        "email": "example@example.com"
    }


user_json = {
    "full_name": "Наполеон Бонапарт",
    "products": [
        {"name": "Сіль", "quantity": 3},
        {"name": "Цукерки", "quantity": 20}
    ],
    "address": {
        "street": "Бонапартова",
        "number": 123,
        "city": {
            "name": "Париж",
            "country": {
                "name": "Франція",
                "code": 340
            }
        }
    },
    "email": "napoleon@example.com"
}

#user = User.model_validate(user_json)

#print(f"{user = }")