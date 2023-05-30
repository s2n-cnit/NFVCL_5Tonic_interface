from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Optional
import logging

def create_logger(name: str) -> logging.getLogger:
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger

logger = create_logger("fiveTonic Simulator")

class OnboardModel(BaseModel):
    """
    Message model for Onboard operation
    """
    nsdId: str = "1" # only RAN, 5GC
    nsName: str = "Ford Slice"
    nsDescription: str = "Network Service for Ford deployment"

class RadioSliceProfileModel(BaseModel):
    site: str = "FORD" # 5Tonic, Innovalia, * FORD *
    coverageArea: str = "FORD_ENGINE_PLANT"
    radioAccessTEchnology: str = "NR" # 4G, mmW, * NR *
    sST: str = "eMBB" # URLLC, mMTC, * eMBB *
    latency: int = 1 # OWD in ms
    uLThptPerSlice: Optional[int] #uplinkth: int # bps
    dLThptPerSlice: Optional[int] #downlinkth: int # bps

class InstantiateModel(BaseModel):
    """
    Message model for NS Instantiate operation
    """
    flavourId: str = "normal"
    radioSliceProfile: RadioSliceProfileModel = RadioSliceProfileModel()

fiveTonicRouter = APIRouter(
        prefix="",
        tags=["fiveTonicSimulator"],
        responses={404: {"description": "Not found"}}
)

@fiveTonicRouter.post("/nslcm/v1/ns_instances")
async def onboard(payload: BaseModel):
    logger.info("Onboard")
    logger.info("Payload: {}".format(payload))
    return {
            "id": "123456",
            "nsInstanceName": "EMBB000001",
            "nsInstanceDescription": "EMBB000001",
            "nsdId": "1",
            "nsdInfoId": "1",
            "nsState": "INSTANTIATED"
        }

@fiveTonicRouter.get("/nslcm/v1/ns_instances")
async def queryNsList():
    logger.info("Query NS List")
    return [
        {
            "id": "09876",
            "nsInstanceName": "EMBB000002",
            "nsInstanceDescription": "EMBB000002",
            "nsdId": "1",
            "nsdInfoId": "1",
            "nsState": "INSTANTIATED"
        },
        {
            "id": "123456",
            "nsInstanceName": "EMBB000001",
            "nsInstanceDescription": "EMBB000001",
            "nsdId": "1",
            "nsdInfoId": "1",
            "nsState": "INSTANTIATED"
        }
        ]

@fiveTonicRouter.get("/nslcm/v1/ns_instances/{nsId}")
async def queryNs(nsId: str):
    logger.info("Query NS")
    logger.info("nsId: {}".format(nsId))
    return {
            "id": "123456",
            "nsInstanceName": "EMBB000001",
            "nsInstanceDescription": "EMBB000001",
            "nsdId": "1",
            "nsdInfoId": "1",
            "nsState": "INSTANTIATED"
    }


@fiveTonicRouter.post("/nslcm/v1/ns_instances/{nsId}/instantiate")
async def instantiateNs(nsId: str, payload: BaseModel):
    logger.info("Instantiate NS")
    logger.info("Payload: {}".format(payload))
    return {}

@fiveTonicRouter.get("/nslcm/v1/ns_lcm_op_occs")
async def queryNsLcmOpOccList():
    logger.info("Query NsLCMOpOcc List")
    return [
            {
                "id": "asdfgh",
                "operationState": "PROCESSING",
                "stateEnteredTime": "",
                "nsInstanceId": "56789",
                "lcmOperationType": "INSTANTIATE",
                "startTime": "",
                "isAutomaticInvocation": True,
                "isCancelPending": False,
                "_links": { "self": "", "nsInstance": ""}
            },
            {
                "id": "qwerty",
                "operationState": "COMPLETED",
                "stateEnteredTime": "",
                "nsInstanceId": "123456",
                "lcmOperationType": "INSTANTIATE",
                "startTime": "",
                "isAutomaticInvocation": True,
                "isCancelPending": False,
                "_links": { "self": "", "nsInstance": ""}
            }
        ]

@fiveTonicRouter.get("/nslcm/v1/ns_lcm_op_occs/{lcmOpOccId}")
async def queryNsLcmOpOcc(lcmOpOccId: str):
    logger.info("Query NsLCMOpOcc")
    logger.info("lcmOpOccId: {}".format(lcmOpOccId))
    return {
                "id": "qwerty",
                "operationState": "COMPLETED",
                "stateEnteredTime": "",
                "nsInstanceId": "123456",
                "lcmOperationType": "INSTANTIATE",
                "startTime": "",
                "isAutomaticInvocation": True,
                "isCancelPending": False,
                "_links": { "self": "", "nsInstance": ""}
            }

@fiveTonicRouter.post("/nslcm/v1/ns_instances/{nsId}/terminate")
async def terminateNs(nsId: str, payload: BaseModel):
    logger.info("Terminate NS")
    logger.info("nsId: {}".format(nsId))
    logger.info("Payload: {}".format(payload))
    return {}

@fiveTonicRouter.delete("/nslcm/v1/ns_instances/{nsId}")
async def deleteNs(nsId: str, payload: BaseModel):
    logger.info("Delete NS")
    logger.info("nsId: {}".format(nsId))
    logger.info("Payload: {}".format(payload))
    return {}

app = FastAPI(
    title="fiveTonic Simulator",
    version="0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(fiveTonicRouter)
