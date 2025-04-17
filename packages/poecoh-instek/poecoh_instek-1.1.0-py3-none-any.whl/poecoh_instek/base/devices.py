from .modes import *
import sys
from typing import overload
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

    @overload
    def __init__(self, *, comm: Comm): ...

    @overload
    def __init__(self, *, port: str, baud: int, identity: Identity): ...

    def __init__(
            self, 
            *,
            port: str | None = None,
            comm: Comm | None = None,
            baud: int | None = None,
    ):
        if comm is not None:
            self._comm = comm
            return
        if port is not None and baud is not None:
            self._comm = Comm(port, baud)
            return
        if port is not None:
            for baud in [115200, 57600, 9600]:
                try:
                    self._comm = Comm(port, baud)
                    return
                except:
                    self._comm.close()
                    continue
        raise InstekException("Failed to instantiate port")

    @property
    def manufacturer(self) -> str:
        return self._comm.id.manufacturer

    @property
    def model(self) -> str:
        return self._comm.id.model

    @property
    def serial(self) -> str:
        return self._comm.id.serial

    @property
    def firmware(self) -> str:
        return self._comm.id.firmware

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

    def independent(self) -> Independent:
        return Independent(self._comm)

    def series(self) -> Series:
        return Series(self._comm)

    def series_common(self) -> SeriesCommon:
        return SeriesCommon(self._comm)

    def parallel(self) -> Parallel:
        return Parallel(self._comm)

    def close(self) -> None:
        self._comm.close()

    def baud(self, rate: int) -> None:
        self._comm.baud(rate)

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
        for baud in [115200, 57600, 9600]:
            try:
                comm = Comm(port_id, baud)
                cls = model_map[comm.id.model]
                instance = cls(comm=comm)
                found.append(instance)
            except:
                continue
    return found
