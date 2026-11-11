import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime
import logging


# ==========================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ==========================================================

logging.basicConfig(
    filename="SIGCSR.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ErrorSistema(Exception):
    """Excepcion general del sistema."""
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass


class OperacionNoPermitidaError(ErrorSistema):
    pass


# ==========================================================
# CLASE ABSTRACTA ENTIDAD
# ==========================================================

class Entidad(ABC):

    def __init__(self, identificador):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)

        if not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        if not documento.strip() or not documento.isdigit():
            raise DatosInvalidosError(
                "El documento debe contener solamente numeros."
            )

        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo electronico no es valido.")

        if not telefono.strip().isdigit():
            raise DatosInvalidosError(
                "El telefono debe contener solamente numeros."
            )

        self._nombre = nombre.strip()
        self._documento = documento.strip()
        self._correo = correo.strip()
        self._telefono = telefono.strip()

    @property
    def nombre(self):
        return self._nombre

    @property
    def documento(self):
        return self._documento

    def mostrar_informacion(self):
        return (
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self._nombre}\n"
            f"Documento: {self._documento}\n"
            f"Correo: {self._correo}\n"
            f"Telefono: {self._telefono}"
        )
