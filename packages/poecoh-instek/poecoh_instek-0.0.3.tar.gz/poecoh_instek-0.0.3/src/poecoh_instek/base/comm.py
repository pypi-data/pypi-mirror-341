from time import sleep
from serial import Serial
from typing import overload

class InstekException(BaseException):
    pass


class Status:
    ch1_cc: bool
    ch2_cc: bool
    beep: bool
    output: bool

    def __init__(self, string: str):
        self.ch1_cc = string[0] == "0"
        self.ch2_cc = string[1] == "0"
        self.beep = string[4] == "1"
        self.output = string[5] == "1"


class Identity:
    manufacturer: str
    model: str
    serial: str
    firmware: str

    def __init__(self, string: str):
        if not string.startswith("GW"):
            raise InstekException("Invalid Identity")
        strings = string.split(",")
        self.manufacturer = strings[0]
        self.model = strings[1]
        self.serial = strings[2][3:]
        self.firmware = strings[3]


class Comm:
    sp: Serial

    def __init__(self, port: str, baud: int):
        self.sp = Serial(port, baud, timeout=0.08, write_timeout=0.01)

    def open(self) -> None:
        if not self.sp.is_open:
            self.sp.open()
            while not self.sp.is_open:
                sleep(0.01)

    def close(self) -> None:
        self.sp.close()

    def write(self, string: str) -> None:
        self.open()
        _ = self.sp.write(f"{string[:14]}'\n".encode())
        sleep(0.01)

    def read(self, timeout: float) -> str | None:
        self.open()
        self.sp.timeout = timeout
        response = self.sp.readline().decode().strip()
        return response if len(response) else None

    def error(self) -> None:
        response = self.read(timeout=1)
        if response is None:
            raise Exception("Instek: Could not get last error")
        if response.lower() == "no error.":
            return None
        raise InstekException(f"Instek: {response}")

    def purge(self) -> None:
        try:
            _ = self.sp.read_all()
        except:
            pass
        _ = self.sp.write(b"\n")
        try:
            self.clear_errors()
            while True:
                if len(self.sp.readline()) == 0:
                    break
        except:
            pass

    def clear_errors(self) -> None:
        while True:
            try:
                self.error()
                return
            except InstekException:
                continue
            except Exception as e:
                raise e

    def command(self, string: str, timeout: float) -> str | None:
        self.write(string)
        line = self.read(timeout=timeout)
        self.error()
        return line

    @overload
    def voltage(self, channel: int) -> float: ...

    @overload
    def voltage(self, channel: int, value: float) -> None: ...

    def voltage(self, channel: int, value: float | None = None) -> float | None:
        if value is None:
            return float(requireResponse(self.command(f"VOUT{channel}?", 0.05))[:-1])
        _ = self.command(f"VSET{channel}:{round(min(value, 30), 3)}", 0.05)

    @overload
    def current(self, channel: int) -> float: ...

    @overload
    def current(self, channel: int, value: float) -> None: ...

    def current(self, channel: int, value: float | None = None) -> float | None:
        if value is None:
            return float(requireResponse(self.command(f"IOUT{channel}?", 0.05))[:-1])
        _ = self.command(f"ISET{channel}:{round(min(value, 3), 3)}", 0.05)

    def status(self) -> Status:
        return Status(requireResponse(self.command("STATUS?", 0.05)))

    def identity(self) -> Identity:
        return Identity(requireResponse(self.command("*IDN?", 0.05)))

    def baud(self) -> None:
        _ = self.command("BAUD0", 0.05)
        self.sp.baudrate = 115200

    def output(self, state: bool) -> None:
        _ = self.command(f"OUT{int(state)}", 0.05)

    def beep(self, state: bool) -> None:
        _ = self.command(f"BEEP{int(state)}", 0.05)

    def tracking(self, mode: int) -> None:
        _ = self.command(f"TRACK{mode}", 0.05)

    @staticmethod
    def test(port: str) -> Identity | None:
        for baud in [115200, 57600, 9600]:
            instance = Comm(port, baud)
            instance.purge()
            try:
                id = instance.identity()
                instance.close()
            except:
                instance.close()
                continue
            return id
        return None


def requireResponse(response: str | None) -> str:
    if response is None:
        raise InstekException("Expected Response")
    return response
