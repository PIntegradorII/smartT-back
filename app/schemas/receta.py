from pydantic import BaseModel

class RecipeRequest(BaseModel):
    ingredient_name: str
    quantity: float
    unit: str
    # Otros campos del esquema