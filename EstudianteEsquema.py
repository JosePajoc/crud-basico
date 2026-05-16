from pydantic import BaseModel, ConfigDict, Field

class Estudiante(BaseModel):
    #convertir objetos de clases normales a nuestro modelo Pydantic
    model_config = ConfigDict(from_attributes=True)

    codigoPersonal: str = Field(min_length=7, max_length=9)
    nombre: str = Field(min_length=1, max_length=20)
    grado: str  = Field(min_length=1)
    direccion: str | None = None   #Permite que sea opcional
    fechaInscripcion: str

class EstudianteRespuesta(BaseModel):
    nombre: str
    mensaje: str

