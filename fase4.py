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


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(Entidad, ABC):

    def __init__(self, identificador, nombre, tarifa):
        super().__init__(identificador)

        if not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio es obligatorio."
            )

        if tarifa <= 0:
            raise DatosInvalidosError(
                "La tarifa debe ser mayor que cero."
            )

        self._nombre = nombre.strip()
        self._tarifa = tarifa
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = bool(estado)

    # CORRECCION IMPORTANTE:
    # Servicio implementa el metodo abstracto de Entidad.
    # Las clases hijas heredan este metodo.
    def mostrar_informacion(self):
        estado = "Disponible" if self._disponible else "No disponible"

        return (
            f"Codigo: {self.identificador}\n"
            f"Nombre: {self._nombre}\n"
            f"Tarifa por hora: ${self._tarifa:,.0f}\n"
            f"Estado: {estado}\n"
            f"Descripcion: {self.describir_servicio()}"
        )

    # Sobrecarga simulada mediante parametros opcionales.
    # Permite calcular el costo con impuesto y descuento.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )

        costo = self.calcular_costo_base(duracion)
        costo_con_impuesto = costo + (costo * impuesto / 100)
        costo_final = costo_con_impuesto - (
            costo_con_impuesto * descuento / 100
        )

        return costo_final

    @abstractmethod
    def calcular_costo_base(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass
