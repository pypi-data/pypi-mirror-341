from time import sleep
from serial import Serial
from typing import overload

class InstekException(BaseException):
    pass

class NoResponse(InstekException):
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
    id: Identity
    debug: bool = False

    def __init__(self, port: str, baud: int):
        self.sp = Serial(port, baud, timeout=0.08, write_timeout=0.01)
        self.purge()
        self.id = self.identity()

    def open(self) -> None:
        if not self.sp.is_open:
            self.sp.open()
            while not self.sp.is_open:
                sleep(0.01)

    def close(self) -> None:
        self.sp.close()

    def write(self, string: str) -> None:
        self.open()
        _ = self.sp.write(f"{string[:14]}\n".encode(encoding="utf-8", errors="strict"))
        # print(f"-> {string}")
        sleep(0.01)

    def read(self, timeout: float) -> str | None:
        self.open()
        self.sp.timeout = timeout
        response = self.sp.readline().decode().strip()
        # print(f"<- {response}")
        return response if len(response) else None

    def check_error_buffer(self) -> None:
        self.write("ERR?")
        response = self.read(timeout=0.1)
        if self.debug:
            print(f"ERR?: {response}")
        if response is None:
            raise NoResponse("Could not get last error")
        if response == "No Error.":
            return None
        raise InstekException(response)

    def purge(self) -> None:
        # Yes, I know, it's complete overkill, but this has been a giant
        # fucking pain in the ass.
        self.write("")
        self.sp.flush()
        self.sp.reset_input_buffer()
        self.sp.reset_output_buffer()
        self.purge_input_buffer(limit=10)
        self.purge_errors(limit=10)

    def purge_input_buffer(self, limit: int) -> None:
        iterations = 0
        while iterations < limit:
            try:
                if self.read(timeout=0.1) is None:
                    return
            except:
                iterations += 1
        raise InstekException("Purge loop")

    def purge_errors(self, limit: int) -> None:
        iterations = 0
        while iterations < limit:
            try:
                self.check_error_buffer()
                return
            except NoResponse:
                raise
            except:
                iterations += 1
        raise InstekException("Error loop")

    def command(self, string: str, timeout: float) -> str | None:
        self.write(string)
        line = self.read(timeout=timeout)
        if self.debug:
            print(f"{string}: {line}")
        self.check_error_buffer()
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
        return Identity(requireResponse(self.command("*IDN?", 1)))

    def baud(self, rate: int) -> None:
        match rate:
            case 115200:
                rate_enum = 0
            case 57600:
                rate_enum = 1
            case 9600:
                rate_enum = 2
            case _:
                raise InstekException("Baud unsupported")
        string = f"BAUD{rate_enum}"
        self.write(string)
        self.sp.baudrate = rate
        sleep(0.05)
        response = self.read(timeout=0.05)
        if self.debug:
            print(f"{string}: {response}")
        self.check_error_buffer()

    def output(self, state: bool) -> None:
        _ = self.command(f"OUT{int(state)}", 0.05)

    def beep(self, state: bool) -> None:
        _ = self.command(f"BEEP{int(state)}", 0.05)

    def tracking(self, mode: int) -> None:
        _ = self.command(f"TRACK{mode}", 0.05)

def requireResponse(response: str | None) -> str:
    if response is None:
        raise InstekException("Expected Response")
    return response
