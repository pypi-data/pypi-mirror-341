from dataclasses import dataclass, field
from typing import Any

from sthg_common_base.utils.constants import Constants


@dataclass
class AccessInfo:
    header: Any
    process_time: Any
    re_code: str
    busi_code: str
    busi_msg: str
    moduler_func_line: str
    param_input: Any
    resp_data: Any
    log_time: Any
    custom_stack: str

    _header: Any = field(init=False, default=Constants.Str_Place)
    _process_time: Any = field(init=False, default=Constants.Str_Place)
    _re_code: str = field(init=False, default=Constants.Str_Place)
    _busi_code: str = field(init=False, default=Constants.Str_Place)
    _busi_msg: str = field(init=False, default=Constants.Str_Place)
    _moduler_func_line: str = field(init=False, default=Constants.Str_Place)
    _param_input: Any = field(init=False, default=Constants.Str_Place)
    _resp_data: Any = field(init=False, default=Constants.Str_Place)
    _log_time: Any = field(init=False, default=Constants.Str_Place)
    _custom_stack: str = field(init=False, default=Constants.Str_Place)

    def __post_init__(self):
        self._header = self.header
        self._process_time = self.process_time
        self._re_code = self.re_code
        self._busi_code = self.busi_code
        self._busi_msg = self.busi_msg
        self._moduler_func_line = self.moduler_func_line
        self._param_input = self.param_input
        self._resp_data = self.resp_data
        self._log_time = self.log_time
        self._custom_stack = self.custom_stack

    @property
    def header(self) -> Any:
        return self._header if self._header is not None else '-'

    @header.setter
    def header(self, value: Any):
        self._header = value

    @property
    def process_time(self) -> Any:
        return self._process_time if self._process_time is not None else '-'

    @process_time.setter
    def process_time(self, value: Any):
        self._process_time = value

    @property
    def re_code(self) -> str:
        return self._re_code if self._re_code is not None else '-'

    @re_code.setter
    def re_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("re_code must be a string")
        self._re_code = value

    @property
    def busi_code(self) -> str:
        return self._busi_code if self._busi_code is not None else '-'

    @busi_code.setter
    def busi_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("busi_code must be a string")
        self._busi_code = value

    @property
    def busi_msg(self) -> str:
        return self._busi_msg if self._busi_msg is not None else '-'

    @busi_msg.setter
    def busi_msg(self, value: str):
        if not isinstance(value, str):
            raise TypeError("busi_msg must be a string")
        self._busi_msg = value

    @property
    def moduler_func_line(self) -> str:
        return self._moduler_func_line if self._moduler_func_line is not None else '-'

    @moduler_func_line.setter
    def moduler_func_line(self, value: str):
        if not isinstance(value, str):
            raise TypeError("moduler_func_line must be a string")
        self._moduler_func_line = value

    @property
    def param_input(self) -> Any:
        return self._param_input if self._param_input is not None else '-'

    @param_input.setter
    def param_input(self, value: Any):
        self._param_input = value

    @property
    def resp_data(self) -> Any:
        return self._resp_data if self._resp_data is not None else '-'

    @resp_data.setter
    def resp_data(self, value: Any):
        self._resp_data = value

    @property
    def log_time(self) -> Any:
        return self._log_time if self._log_time is not None else '-'

    @log_time.setter
    def log_time(self, value: Any):
        self._log_time = value

    @property
    def custom_stack(self) -> str:
        return self._custom_stack if self._custom_stack is not None else '-'

    @custom_stack.setter
    def custom_stack(self, value: str):
        if not isinstance(value, str):
            raise TypeError("custom_stack must be a string")
        self._custom_stack = value