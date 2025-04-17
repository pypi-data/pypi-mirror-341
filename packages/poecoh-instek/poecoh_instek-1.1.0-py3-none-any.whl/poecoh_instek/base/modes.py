from .channels import ChannelI, ChannelS, Channel4, Channel3, Comm, Identity, InstekException
__all__ = ["Comm", "Independent", "Series", "SeriesCommon", "Parallel", "Identity", "InstekException", "Channel4", "Channel3"]

class BaseMode:
    _comm: Comm

    def __init__(self, comm: Comm):
        self._comm = comm

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
        return self._comm.beep(state)


class Independent(BaseMode):

    def __init__(self, comm: Comm):
        super().__init__(comm)
        comm.tracking(0)

    @property
    def ch1(self) -> ChannelI:
        return ChannelI(self._comm, 1)

    @property
    def ch2(self) -> ChannelI:
        return ChannelI(self._comm, 2)

class Series(BaseMode):

    def __init__(self, comm: Comm):
        super().__init__(comm)
        comm.tracking(1)
        comm.current(2, 3)

    @property
    def voltage(self) -> float:
        return round(self._comm.voltage(1) * 2, 3)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self._comm.voltage(1, value / 2)

    @property
    def current(self) -> float:
        return self._comm.current(1)

    @current.setter
    def current(self, value: float) -> None:
        self._comm.current(1, value)

    @property
    def cc(self) -> bool:
        return self._comm.status().ch1_cc

class SeriesCommon(BaseMode):

    def __init__(self, comm: Comm):
        super().__init__(comm)
        comm.tracking(1)

    @property
    def voltage(self) -> float:
        return round(self._comm.voltage(1) * 2, 3)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self._comm.voltage(1, value / 2)

    @property
    def ch1(self) -> ChannelS:
        return ChannelS(self._comm, 1)

    @property
    def ch2(self) -> ChannelS:
        return ChannelS(self._comm, 2)



class Parallel(BaseMode):

    def __init__(self, comm: Comm):
        super().__init__(comm)
        comm.tracking(2)

    @property
    def voltage(self) -> float:
        return self._comm.voltage(1)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self._comm.voltage(1, value)

    @property
    def current(self) -> float:
        return round(self._comm.current(1) * 2, 3)

    @current.setter
    def current(self, value: float) -> None:
        self._comm.current(1, value / 2)

    @property
    def cc(self) -> bool:
        return self._comm.status().ch1_cc
