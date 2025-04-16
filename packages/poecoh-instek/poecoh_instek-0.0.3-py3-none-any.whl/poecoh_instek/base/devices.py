from .modes import *
import sys
if sys.platform == "win32":
    from serial.tools.list_ports_windows import comports
elif sys.platform == "linux":
    from serial.tools.list_ports_linux import comports
elif sys.platform == "darwin":
    from serial.tools.list_ports_osx import comports
else:
    raise Exception("Unsupported os")

class GPD:
    _comm: Comm
    __identity: Identity

    def __init__(self, port: str, identity: Identity | None = None):
        for baud in [115200, 57600, 9600]:
            try:
                self._comm = Comm(port, baud)
                if identity is None:
                    self._comm.purge()
                    identity = self._comm.identity()
                self._comm.baud()
                self.__identity = identity
                return
            except:
                self._comm.close()
                continue
        raise InstekException("Failed to instantiate port")

    @property
    def manufacturer(self) -> str:
        return self.__identity.manufacturer

    @property
    def model(self) -> str:
        return self.__identity.model

    @property
    def serial(self) -> str:
        return self.__identity.serial

    @property
    def firmware(self) -> str:
        return self.__identity.firmware

    @property
    def output(self) -> bool:
        return self._comm.status().output

    @output.setter
    def output(self, state: bool) -> None:
        self._comm.output(state)

    @property
    def beep(self) -> bool:
        return self._comm.status().beep

    @beep.setter
    def beep(self, state: bool) -> None:
        self._comm.beep(state)

    @property
    def independent(self) -> Independent:
        return Independent(self._comm)

    @property
    def series(self) -> Series:
        return Series(self._comm)

    @property
    def series_common(self) -> SeriesCommon:
        return SeriesCommon(self._comm)

    @property
    def parallel(self) -> Parallel:
        return Parallel(self._comm)

    def close(self) -> None:
        self._comm.close()

class GPD2303(GPD):
    pass


class GPD3303(GPD):
    pass

class GPD4303(GPD):

    @property
    def ch3(self) -> Channel3:
        return Channel3(self._comm)

    @property
    def ch4(self) -> Channel4:
        return Channel4(self._comm)

model_map: dict[str, type[GPD2303] | type[GPD3303] | type[GPD4303]] = {
    "GPD-2303S": GPD2303,
    "GPD-3303S": GPD3303,
    "GPD-4303S": GPD4303,
}

def find() -> list[GPD2303 | GPD3303 | GPD4303]:
    found: list[GPD2303 | GPD3303 | GPD4303] = []
    port_id = ""
    for port_info in comports():
        if port_info.manufacturer != "FTDI":
            continue
        match sys.platform:
            case "win32":
                port_id = port_info.device
            case "linux" | "darwin":
                port_id = f"/dev/{port_info.name}"
            case _:
                raise Exception("OS not supported")
        try:
            id = Comm.test(port_id)
            if id is None:
                continue
            cls = model_map[id.model]
            instance: GPD = cls(port_id, id)
            instance.close()
            found.append(instance)
        except:
            pass
    return found
