"""fiveTonicModel

5Tonic Interface NFVCL module

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
from __future__ import annotations
from typing import Optional, Union
from pydantic import BaseModel
from models.blue5gModel import Free5gck8sBlueCreateModel, MiniFree5gcModel
from utils.util import SstConvertion
from utils.fiveqi import fiveqiTable
from utils.util import BandwidthConvertion


class OnboardModel(BaseModel):
    """
    Message model for Onboard operation
    """
    nsdId: str = "1" # only RAN, 5GC
    nsName: str = "Ford Slice"
    nsDescription: str = "Network Service for Ford deployment"

    @classmethod
    def fromFree5GcModel(cls, msg: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> OnboardModel:
        onboardObject = OnboardModel()
        sliceName = "{}{}".format(msg.config.sliceProfiles[0].sliceType, msg.config.sliceProfiles[0].sliceId)
        onboardObject.nsdId = 1
        onboardObject.nsName = sliceName
        onboardObject.nsDescription = sliceName
        return onboardObject


class RadioSliceProfileModel(BaseModel):
    site: str = "FORD_VALENCIA" # 5Tonic, Innovalia, * FORD_VALENCIA *
    coverageArea: str = "FORD_INDOOR" # ENGINE_INDOOR or ENGINE_OUTDOOT
    radioAccessTEchnology: str = "NR" # 4G, mmW, * NR *
    sST: str = "eMBB" # URLLC, mMTC, * eMBB *
    latency: int = 1 # OWD in ms
    uLThptPerSlice: Optional[int] #uplinkth: int # bps
    dLThptPerSlice: Optional[int] #downlinkth: int # bps

    @classmethod
    def fromFree5GcModel(cls, msg: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> RadioSliceProfileModel:
        radioSliceProfileObject = RadioSliceProfileModel()
        radioSliceProfileObject.site = "FORD_VALENCIA"
        radioSliceProfileObject.coverageArea = "ENGINE_INDOOR" # ENGINE_INDOOR or ENGINE_OUTDOOR
        radioSliceProfileObject.radioAccessTEchnology = "NR"
        radioSliceProfileObject.sST = SstConvertion.to5Tonic(msg.config.sliceProfiles[0].sliceType)
        radioSliceProfileObject.latency = next((item["packetDelayBudget"] for item in fiveqiTable
                                                if item["value"]==int(msg.config.network_endpoints.data_nets[0].default5qi)),9)
        radioSliceProfileObject.uLThptPerSlice = BandwidthConvertion.convert(
            msg.config.sliceProfiles[0].profileParams.sliceAmbr, "bps")
        radioSliceProfileObject.dLThptPerSlice = BandwidthConvertion.convert(
            msg.config.sliceProfiles[0].profileParams.sliceAmbr, "bps")
        return radioSliceProfileObject

class RadioSliceProfileObject(BaseModel):
    radioSliceProfile: RadioSliceProfileModel = RadioSliceProfileModel() 

    @classmethod
    def fromFree5GcModel(cls, msg: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> RadioSliceProfileObject:
        radioSliceProfileObject = RadioSliceProfileObject()
        radioSliceProfileObject.radioSliceProfile = RadioSliceProfileModel.fromFree5GcModel(msg)
        return radioSliceProfileObject

class InstantiateModel(BaseModel):
    """
    Message model for NS Instantiate operation
    """
    flavourId: str = "normal"
    sapData: List[RadioSliceProfileObject] = []

    @classmethod
    def fromFree5GcModel(cls, msg: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> InstantiateModel:
        instantiateObject = InstantiateModel()
        instantiateObject.flavourId = "normal"
        instantiateObject.sapData.append(RadioSliceProfileObject.fromFree5GcModel(msg))
        return instantiateObject































