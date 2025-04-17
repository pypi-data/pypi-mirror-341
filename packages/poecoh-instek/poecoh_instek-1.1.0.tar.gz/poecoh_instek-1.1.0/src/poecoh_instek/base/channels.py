from .comm import Comm, InstekException, Identity

__all__ = ["Comm", "InstekException", "Channel3", "Channel4", "ChannelI", "ChannelS", "Identity"]

class Channel3:
    __comm: Comm

    def __init__(self, comm: Comm):
        self.__comm = comm

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(3)
    
    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(3, min(value, 5))

    @property
    def current(self) -> float:
        return self.__comm.current(3)
    
    @current.setter
    def current(self, value: float) -> None:
        return self.__comm.current(3, min(value, 3))
    
class Channel4:
    __comm: Comm

    def __init__(self, comm: Comm):
        self.__comm = comm

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(4)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(4, min(value, 5))

    @property
    def current(self) -> float:
        return self.__comm.current(4)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(4, min(value, 3))


class ChannelI:
    __comm: Comm
    __number: int

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(self.__number)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(self.__number, value)

    @property
    def current(self) -> float:
        return self.__comm.current(self.__number)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(self.__number, value)

    @property
    def cc(self) -> bool:
        value = getattr(self.__comm.status(), f"ch{self.__number}_cc")
        if isinstance(value, bool):
            return value
        raise InstekException("Expected bool")

    def __init__(self, comm: Comm, number: int):
        self.__comm = comm
        self.__number = number


class ChannelS:
    __comm: Comm
    __number: int

    @property
    def current(self) -> float:
        return self.__comm.current(self.__number)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(self.__number, value)

    def __init__(self, comm: Comm, number: int):
        self.__comm = comm
        self.__number = number
