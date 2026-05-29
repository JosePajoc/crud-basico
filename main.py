from fastapi import FastAPI, HTTPException, status
from EstudianteEsquema import Estudiante, EstudianteRespuesta
#proyecto desplegado en Render
#datos de prueba
datosPrueba = [
    {
        "codigoPersonal": "ABC123AB",
        "nombre": "José Pajoc",
        "grado": "Bachillerato",
        "direccion": "Guatemala",
        "fechaInscripcion": "02/01/2026"
    },
    {
        "codigoPersonal": "QWE123QW",
        "nombre": "nombre de QWE",
        "grado": "Básicos",
        "direccion": "ciudad de QWE",
        "fechaInscripcion": "05/01/2026"
    },
    {
        "codigoPersonal": "ZXC123ZX",
        "nombre": "nombre de ZXC",
        "grado": "Primaria",
        "direccion": "ciudad de ZXC",
        "fechaInscripcion": "10/01/2026"
    }
]

app = FastAPI(
    title="CRUD",
    description="API básica para gestionar datos de estudiantes, la información se almacena en una lista por lo cual los datos son temporales, estos son mis primeros pasos en el desarrollo Backend. Esto se logró con el lenguaje de programación Python y el framework FastAPI",
    version="1.0.0",
    contact={
        "name": "José Pajoc",
        "email": "jose.ernesto.pajoc@gmail.com",
        "url": "https://jose-pajoc-dev.onrender.com/",
    },
    license_info={
        "name": "MIT"}
    )

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo, estos son mis primeros pasos en el mundo del Backend con la ayuda de Fast API"}


@app.get("/estudiantes", response_model=list[Estudiante], tags=["CRUD Básico"])
def estudiantes():
    return datosPrueba


@app.get("/estudiantes/{codigoPersonal}", response_model=Estudiante, tags=["CRUD Básico"])
def estudianteID(codigoPersonal: str):
    for elemento in datosPrueba:
        if elemento["codigoPersonal"] == codigoPersonal:
            return elemento
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")


@app.post("/estudiantes/nuevo", response_model=EstudianteRespuesta, status_code=status.HTTP_201_CREATED, tags=["CRUD Básico"])
def estudianteNuevo(entradaRegistro: Estudiante):
    nuevoRegistro = {
        "codigoPersonal": entradaRegistro.codigoPersonal,
        "nombre": entradaRegistro.nombre,
        "grado": entradaRegistro.grado,
        "direccion": entradaRegistro.direccion,
        "fechaInscripcion": entradaRegistro.fechaInscripcion
    }
    encontrado, _ = buscarEstudiante(nuevoRegistro["codigoPersonal"])
    if encontrado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El código ya existe")
    
    datosPrueba.append(nuevoRegistro)
    return {"nombre": nuevoRegistro["nombre"], "mensaje": "Almacenado con éxito"}

#----------------------------------------
def buscarEstudiante(codigoPersonal: str):
    encontrado = False
    posicion = -1
    for i in range(len(datosPrueba)):
        if datosPrueba[i]["codigoPersonal"] == codigoPersonal:
            encontrado = True
            posicion = i
            break
    return encontrado, posicion
#----------------------------------------


@app.put("/estudiantes/{codigoPersonal}", response_model=EstudianteRespuesta, status_code=status.HTTP_200_OK, tags=["CRUD Básico"])
def actualizarEstudiante(codigoPersonal: str, estudiante: Estudiante):
    encontrado, posicion = buscarEstudiante(codigoPersonal)
    if encontrado:
        datosPrueba[posicion]["nombre"] = estudiante.nombre
        datosPrueba[posicion]["grado"] = estudiante.grado
        datosPrueba[posicion]["direccion"] = estudiante.direccion
        datosPrueba[posicion]["fechaInscripcion"] = estudiante.fechaInscripcion
        return {"nombre": estudiante.nombre, "mensaje": "Actualizado con éxito"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")


@app.delete("/estudiantes/{codigoPersonal}", status_code=status.HTTP_200_OK, tags=["CRUD Básico"])
def eliminarEstudiante(codigoPersonal: str):
    encontrado, posicion = buscarEstudiante(codigoPersonal)
    if encontrado:
        datosPrueba.pop(posicion)
        return {"mensaje": "Dato eliminado"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
