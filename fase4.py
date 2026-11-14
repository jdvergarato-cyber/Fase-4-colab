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


# ==========================================================
# SERVICIO 1: RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, tarifa, capacidad):
        super().__init__(identificador, nombre, tarifa)

        if capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad debe ser mayor que cero."
            )

        self._capacidad = capacidad
        self.validar_parametros()

    def calcular_costo_base(self, duracion):
        return self._tarifa * duracion 

    def describir_servicio(self):
        return (
            f"Sala: {self._nombre} | "
            f"Capacidad: {self._capacidad} personas"
        )

    def validar_parametros(self):
        if self._capacidad <= 0:
            raise DatosInvalidosError("La capacidad no es valida.")


# ==========================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, tarifa, cantidad):
        super().__init__(identificador, nombre, tarifa)

        if cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad debe ser mayor que cero."
            )

        self._cantidad = cantidad
        self.validar_parametros()

    def calcular_costo_base(self, duracion):
        return self._tarifa * duracion * self._cantidad

    def describir_servicio(self):
        return (
            f"Equipo: {self._nombre} | "
            f"Cantidad: {self._cantidad} unidades"
        )

    def validar_parametros(self):
        if self._cantidad <= 0:
            raise DatosInvalidosError("La cantidad no es valida.")


# ==========================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, identificador, nombre, tarifa, especialidad):
        super().__init__(identificador, nombre, tarifa)

        if not especialidad.strip():
            raise DatosInvalidosError(
                "La especialidad es obligatoria."
            )

        self._especialidad = especialidad.strip()
        self.validar_parametros()

    def calcular_costo_base(self, duracion):
        return self._tarifa * duracion

    def describir_servicio(self):
        return (
            f"Asesoria: {self._nombre} | "
            f"Especialidad: {self._especialidad}"
        )

    def validar_parametros(self):
        if not self._especialidad:
            raise DatosInvalidosError("La especialidad no es valida.")


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es valido.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es valido.")

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no esta disponible."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._fecha = datetime.now()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio ya no esta disponible."
            )

        self._estado = "Confirmada"

    def cancelar(self):
        if self._estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "Esta reserva no se puede cancelar."
            )

        self._estado = "Cancelada"

    def procesar(self):
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Primero debe confirmar la reserva."
            )

        self._estado = "Procesada"

    def calcular_costo(self, impuesto=19, descuento=10):
        try:
            return self._servicio.calcular_costo(
                self._duracion,
                impuesto,
                descuento
            )
        except DatosInvalidosError as error:
            raise ReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio.nombre}\n"
            f"Duracion: {self._duracion} horas\n"
            f"Estado: {self._estado}\n"
            f"Fecha: {self._fecha.strftime('%d/%m/%Y %H:%M')}"
        )


# ==========================================================
# SISTEMA DE GESTION
# ==========================================================

class SistemaGestion:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

        self.contador_cliente = 1
        self.contador_servicio = 1
        self.contador_reserva = 1

        logging.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, nombre, documento, correo, telefono):
        try:
            for cliente in self.clientes:
                if cliente.documento == documento.strip():
                    raise DatosInvalidosError(
                        "Ya existe un cliente con ese documento."
                    )

            cliente = Cliente(
                f"C{self.contador_cliente:03d}",
                nombre,
                documento,
                correo,
                telefono
            )

        except ErrorSistema:
            logging.exception("Error al registrar cliente.")
            raise

        else:
            self.clientes.append(cliente)
            self.contador_cliente += 1
            logging.info(
                "Cliente registrado: %s",
                cliente.identificador
            )
            return cliente

        finally:
            logging.info("Finalizo el intento de registro de cliente.")

    def crear_servicio(self, tipo, nombre, tarifa, parametro):
        try:
            tarifa = float(tarifa)

            if tarifa <= 0:
                raise DatosInvalidosError(
                    "La tarifa debe ser mayor que cero."
                )

            identificador = f"S{self.contador_servicio:03d}"

            if tipo == "Sala":
                capacidad = int(parametro)
                servicio = ReservaSala(
                    identificador, nombre, tarifa, capacidad
                )

            elif tipo == "Equipo":
                cantidad = int(parametro)
                servicio = AlquilerEquipo(
                    identificador, nombre, tarifa, cantidad
                )

            elif tipo == "Asesoria":
                servicio = AsesoriaEspecializada(
                    identificador, nombre, tarifa, parametro
                )

            else:
                raise DatosInvalidosError(
                    "Seleccione un tipo de servicio valido."
                )

        except (ValueError, TypeError) as error:
            logging.exception(
                "Error en los parametros del servicio."
            )
            raise DatosInvalidosError(
                f"Revise los datos ingresados. Detalle: {error}"
            ) from error

        except ErrorSistema:
            logging.exception("Error al crear servicio.")
            raise

        else:
            self.servicios.append(servicio)
            self.contador_servicio += 1

            logging.info(
                "Servicio creado: %s - %s",
                servicio.identificador,
                servicio.nombre
            )
            return servicio

        finally:
            logging.info("Finalizo el intento de creacion de servicio.")

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            if cliente not in self.clientes:
                raise ReservaError(
                    "El cliente no esta registrado."
                )

            if servicio not in self.servicios:
                raise ReservaError(
                    "El servicio no esta registrado."
                )

            duracion = float(duracion)

            reserva = Reserva(
                f"R{self.contador_reserva:03d}",
                cliente,
                servicio,
                duracion
            )

        except (ValueError, TypeError) as error:
            logging.exception("Duracion de reserva incorrecta.")
            raise DatosInvalidosError(
                f"La duracion no es valida: {error}"
            ) from error

        except ErrorSistema:
            logging.exception("Error al crear reserva.")
            raise

        else:
            self.reservas.append(reserva)
            self.contador_reserva += 1

            logging.info(
                "Reserva creada: %s",
                reserva.identificador
            )
            return reserva

        finally:
            logging.info("Finalizo el intento de creacion de reserva.")


# ==========================================================
# INTERFAZ GRAFICA
# ==========================================================

class AplicacionSoftwareFJ:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Software JV - Gestion Integral by: Jesus vergara")
        self.ventana.geometry("1100x750")
        self.ventana.minsize(900, 650)

        self.sistema = SistemaGestion()
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(
            self.ventana,
            text="SOFTWARE SIGCSR",
            font=("Arial", 22, "bold"),
            fg="#174A75"
        ).pack(pady=5)

        tk.Label(
            self.ventana,
            text="Sistema Integral de Gestion de Clientes, Servicios y Reservas",
            font=("Arial", 11)
        ).pack(pady=3)

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(
            fill="both", expand=True, padx=12, pady=10
        )

        self.tab_clientes = ttk.Frame(self.pestanas)
        self.tab_servicios = ttk.Frame(self.pestanas)
        self.tab_reservas = ttk.Frame(self.pestanas)
        self.tab_pruebas = ttk.Frame(self.pestanas)

        self.pestanas.add(self.tab_clientes, text="Clientes")
        self.pestanas.add(self.tab_servicios, text="Servicios")
        self.pestanas.add(self.tab_reservas, text="Reservas")
        self.pestanas.add(self.tab_pruebas, text="Pruebas del sistema")

        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()
        self.crear_tab_pruebas()

        tk.Label(
            self.ventana,
            text="Software JV | Sistema de gestion sin base de datos",
            fg="gray"
        ).pack(pady=5)
