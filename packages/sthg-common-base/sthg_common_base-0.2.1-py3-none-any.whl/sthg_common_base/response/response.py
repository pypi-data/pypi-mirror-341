from typing import Any, Generic, Optional, TypeVar

from datetime import datetime, date, time
from fastapi.responses import JSONResponse
from pydantic import Field
from decimal import Decimal

import  json

from sthg_common_base.response.httpCodeEnmu import ResponseEnum
from uuid import UUID
from pydantic import BaseModel

from sthg_common_base.response.json_serializer import EnhancedJSONSerializer

T = TypeVar('T')

try:
    from bson import ObjectId
except ImportError:
    ObjectId = None  # 处理未安装pymongo的情况

try:
    import numpy as np
except ImportError:
    np = None  # 处理未安装numpy的情况

class BaseResponse(Generic[T]):
    code: Optional[int] = Field(ResponseEnum.OK.getHttpCode, description="HTTP 状态码")
    busiCode: Optional[str] = Field(ResponseEnum.OK.getBusiCode, description="业务状态码")
    busiMsg: Optional[str] = Field(ResponseEnum.OK.getBusiMsg, description="业务消息")
    data: Optional[T] = Field(None, description="返回数据")

    def __init__(self, resEnmu: ResponseEnum, data: Any, msg: str = None, *args):
        if msg and args:
            msg = msg.format(*args)
        self.code= resEnmu.getHttpCode
        self.busiCode= resEnmu.getBusiCode
        if msg:
            self.busiMsg = f"{resEnmu.getBusiMsg},{msg}"
        else:
            self.busiMsg = f"{resEnmu.getBusiMsg}"
        self.data=data

    def __call__(self, *args) -> JSONResponse:
        return JSONResponse(status_code=self.code,
                            content={
                                "code": self.code,
                                "busiCode": self.busiCode,
                                "busiMsg": self.busiMsg,
                                "data": self.data if EnhancedJSONSerializer.deep_serialize(self.data) else None,
                            })

    def is_success(self):
        is_success = False
        if self.code < 400:
            is_success = True
        return is_success

    def build_reset_by_resenum(self, data:any, resEnmu: ResponseEnum, msg=None):
        self.code = resEnmu.getHttpCode
        self.busiCode = resEnmu.getBusiCode
        if msg :
            self.busiMsg = f"{resEnmu.getBusiMsg},{msg}"
        else:
            self.busiMsg = resEnmu.getBusiMsg
        self.data = data

    def build_reset_by_resp(self,response: 'BaseResponse', msg=None):
        self.code = response.code
        self.busiCode = response.busiCode
        if msg :
            self.busiMsg = f"{response.busiMsg},{msg}"
        else:
            self.busiMsg = response.busiMsg
        self.data = response.data

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            default=EnhancedJSONSerializer.json_serializer,
            ensure_ascii=False
        )

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "busiCode": self.busiCode,
            "busiMsg": self.busiMsg,
            "data": EnhancedJSONSerializer.deep_serialize(self.data)
        }