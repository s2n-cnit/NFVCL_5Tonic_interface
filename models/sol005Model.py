"""sol005Model

sol 005 models

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
from __future__ import annotations
from typing import List, Optional, Literal, Dict, Union
from pydantic import BaseModel, Field

class NsInstance(BaseModel):
    id: str
    nsInstanceName: str
    nsInstanceDescription: str
    nsdId: str
    nsdInfoId: str
    nsState: Literal["INSTANTIATED", "NOT_INSTANTIATED"]

class NsInstanceList(BaseModel):
    __root__: List[NsInstance]

    @classmethod
    def fromArray(cls, data: List[NsInstance]):
        nsInstanceList = NsInstanceList()
        nsInstanceList.__root__ = data
        return nsInstanceList

class Links(BaseModel):
    self: str
    nsInstance: str

class NsLcmOpOcc(BaseModel):
    id: str
    operationState: Literal["PROCESSING", "COMPLETED", "PARTIALLY_COMPLETED", "FAILED_TEMP", "FAILED",
                            "ROLLING_BACK", "ROLLED_BACK"]
    stateEnteredTime: str
    nsInstanceId: str
    lcmOperationType: Literal["INSTANTIATE", "SCALE", "UPDATE", "TERMINATE", "HEAL"]
    startTime: str
    isAutomaticInvocation: bool
    isCancelPending: bool
    _links: Links

class NsLcmOpOccList(BaseModel):
    __root__: List[NsLcmOpOcc]

    @classmethod
    def fromArray(cls, data: List[NsLcmOpOcc]):
        nsLcmOpOccList = NsLcmOpOccList()
        nsLcmOpOccList.__root__ = data
        return nsLcmOpOccList
