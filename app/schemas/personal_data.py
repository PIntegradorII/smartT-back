from pydantic import BaseModel, EmailStr

# Esquema base para la entrada y validación de datos
class PersonalDataBase(BaseModel):
    user_id: int
    nombre: str
    edad: int
    genero: str
    correo: EmailStr

# Esquema para la creación de datos
class PersonalDataCreate(PersonalDataBase):
    pass

# Esquema para la respuesta de datos, incluyendo el ID
class PersonalDataResponse(PersonalDataBase):
    id: int

    class Config:
        from_attributes  = True

