from fastapi import FastAPI, Body, Query
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()


class Items(BaseModel):
    # name : str = Field(..., example="mobile phone")       ## using example you can show an example value in swagger documentation
    # brand : str = Field(..., example="samsung")
    # price : float = Field(..., example=200.89)
    # taxs : list[int] = Field(..., example=[12, 8, 6])
            ## OR
    name : str
    brand : str
    price : float
    taxs : list[int]

        ### using this model_config also you can show an example value in swagger documentation
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #             "name": "laptop",
    #             "brand": "MSI",
    #             "price": 49863,
    #             "taxs": [12, 8, 6]
    #         }
    #         ]
    #     }
    # }





# @app.put('/update_item/{id}')
# async def update_product(id: int, item: Items):
#     data = {"id": id, **item.dict()}
#     return data




"""
single example 
"""
#         ## like this you can display some example data to user in swagger documentation 
# @app.put('/update_item/{id}')
# async def update_product(id: int, item: Items = Body(..., example={
#                                                                     "name": "laptop",
#                                                                     "brand": "MSI",
#                                                                     "price": 49863,
#                                                                     "taxs": [12, 8, 6]
#                                                                     })):
#     data = {"id": id, **item.dict()}
#     return data






"""
multiple examples
"""
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Items,
        Body(
            examples=[
                {
                    "name": "cap",
                    "brand": "puma",
                    "price": 2363,
                    "taxs": [13.2, 6.2],
                }
            ],
        ),
    ],
    ):
    results = {"item_id": item_id, "item": item}
    return results





"""
using openapi example you can show multiple types of examples .... it will give a dropdown option for user to choose any case 
and check the example
"""
        # like this you can display some example data to user in swagger documentation 
@app.put('/update_item/{id}')
async def update_product(id: int, item: Items = Body(..., 
                                                     openapi_examples={
                                                                "normal" : {
                                                                    "summary": "A normal example",
                                                                    "description": "A **normal** item works correctly.",
                                                                    "value": {
                                                                    "name": "laptop",
                                                                    "brand": "MSI",
                                                                    "price": 49863,
                                                                    "taxs": [12, 8, 6]
                                                                        }
                                                                    },
                                                                "converted" : {
                                                                    "summary":"An example with converted data",
                                                                    "description": "FastAPI can convert str number value to integer",
                                                                    "value" : {
                                                                    "name" : "mobile",
                                                                    "brand": "samsung",
                                                                    "price": "2353.3",
                                                                    "taxs":[3,5,9]
                                                                        }
                                                                    },
                                                                "invalid" : {
                                                                    "summary": "Invalid data summary example",
                                                                    "description": "python can not change alphabate to numbers",
                                                                    "value": {
                                                                    "name": "watch",
                                                                    "brand": "noise",
                                                                    "price": "hundred",
                                                                    "taxs": [1, 4, "five"]
                                                                        }
                                                                    },
                                                                    })):
    data = {"id": id, **item.dict()}
    return data






# @app.put('/update_item/{id}')
# async def update_product(
#     id: int,
#     item: Items = Body(
#         ...,
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "Example with correct types",
#                 "value": {
#                     "name": "laptop",
#                     "brand": "MSI",
#                     "price": 49863,
#                     "taxs": [12, 8, 6]
#                 }
#             },
#             "converted": {
#                 "summary": "An example with summary data",
#                 "description": "FastAPI can convert string number value to float",
#                 "value": {
#                     "name": "mobile",
#                     "brand": "samsung",
#                     "price": 2353.3,
#                     "taxs": [3, 5, 9]
#                 }
#             },
#             "invalid": {
#                 "summary": "Invalid data summary example",
#                 "description": "Python cannot convert non-numeric strings to numbers",
#                 "value": {
#                     "name": "watch",
#                     "brand": "noise",
#                     "price": "hundred",  # This should raise a validation error
#                     "taxs": [1, 4, "five"]  # This should raise a validation error
#                 }
#             }
#         }
#     )
#     ):
#     data = {"id": id, **item.dict()}
#     return data


