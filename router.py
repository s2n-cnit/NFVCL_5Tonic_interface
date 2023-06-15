"""Router

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
import fastapi
import time
import requests
from threading import Thread
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
from models import Free5gck8sBlueCreateModel, MiniFree5gcModel, OnboardModel, \
    InstantiateModel, NsInstance, NsLcmOpOcc
from fiveTonicRestApi import FiveTonicRestApi
from utils import create_logger

fiveTonicParametersFile = "fivetonichost.txt"
logger = create_logger("Router")

northRouter = APIRouter(
    prefix="",
    tags=["NorthRouter"],
    responses={404: {"description": "Not found"}}
)

try:
    with open(fiveTonicParametersFile, "r") as f:
        fiveTonicHost = f.readline().split("\n")[0]
        fiveTonicPort = f.readline().split("\n")[0]
        f.close()
        logger.info("Read from file (\"{}\"): Athonet host-port: {} - {}".format(fiveTonicParametersFile, fiveTonicHost, fiveTonicPort))
except Exception as e:
    logger.error("Impossible to read the file \"{}\"".format(fiveTonicParametersFile))
    raise ValueError("Impossible to read the file \"{}\"".format(fiveTonicParametersFile))

fiveTonicInterface = FiveTonicRestApi(fiveTonicHost, fiveTonicPort)


class RestAnswer202(BaseModel):
    #id: str
    description: str = "operation submitted"
    status: str = "submitted"



def restCallback(callback, requestedOperation, blueId, sessionId, status):
    if callback:
        logger.info("Generating callback message")
        headers = {
                "Content-type": "application/json",
                "Accept": "application/json"
                }
        data = {
                "blueprint":
                {
                    "id": blueId,
                    "type": "Free5GC_K8s"
                },
                "requested_operation": requestedOperation,
                "session_id": blueId,
                "status": status
              }
        r = None
        try:
            r = requests.post(callback, json=data, params=None, verify=False, stream=True, headers=headers)
            return r
        except Exception as e:
            logger.error("Error - posting callback: ", e)
    else:
        logger.info("No callback message is specified")
        return None



def getSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> NsInstance:
    nsList = fiveTonicInterface.nsQueryList()
    nsName = "{}{}".format(
        free5gcMessage.config.sliceProfiles[0].sliceType, free5gcMessage.config.sliceProfiles[0].sliceId
    )
    ns = next((item for item in nsList if item.nsInstanceName == nsName), None)
    return ns


def getLcmOpOcc(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]) -> NsLcmOpOcc:
    nsLcmOpOccList = fiveTonicInterface.nsLcmOpOccQueryList()
    slice = getSlice(free5gcMessage)
    if not slice or not nsLcmOpOccList:
        raise ValueError("Slice not exist")
    return next((item for item in nsLcmOpOccList if item.nsInstanceId == slice.id), None)


def instantiateSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel], id, instantiateObject, blueId, requestedOperation):
    # check if slice is onboarded and then instantiate it
    partialTimer = 0
    totalTime = 600 # 5 minutes in seconds
    clock = 2 # in seconds
    callback = free5gcMessage.callbackURL
    try:
        ns = getSlice(free5gcMessage)
        fiveTonicInterface.nsInstantiate(ns.id, instantiateObject)
        while True:
            time.sleep(clock)
            ns = getSlice(free5gcMessage)
            logger.info("NS: {}".format(ns))
            if ns and ns.nsState.upper() == "INSTANTIATED":
                logger.info("Instantiated")
                if callback != "":
                    restCallback(callback, requestedOperation, blueId, blueId, "ready")
                return
            else:
                logger.info("wait {} seconds...".format(clock))
                time.sleep(clock)
                partialTimer += clock
                if partialTimer == totalTime:
                    logger.info("Operation timed out")
                    if callback != "":
                        restCallback(callback, requestedOperation, blueId, blueId, "failed")
                    return

    except Exception as e:
        logger.warn("Impossible to delete the slice: {}".format(e))
        if callback != "":
            restCallback(callback, requestedOperation, blueId, blueId, "failed")
        raise fastapi.HTTPException(status_code=404, detail="Impossible to delete the slice: {}".format(e))

def deleteSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel], blueId, requestedOperation):
    # check if slice is terminated and then delete it
    partialTimer = 0
    totalTime = 600 # 5 minutes in seconds
    clock = 2 # in seconds
    callback = free5gcMessage.callbackURL
    try:
        while True:
            nsLcmOpOcc = getLcmOpOcc(free5gcMessage)
            if not nsLcmOpOcc:
                logger.warn("the status of the slice is empty")
                raise ValueError("the status of the slice is empty")
            logger.info("nsLcmOpOcc: {}".format(nsLcmOpOcc))
            if nsLcmOpOcc.operationState.upper() == "PROCESSING" \
                    or nsLcmOpOcc.operationState.upper() == "ROLLING_BACK":
                logger.info("Slice in state: {} . Waiting...".format(nsLcmOpOcc.operationState))
                time.sleep(clock)
                partialTimer += clock
                if partialTimer == totalTime:
                    logger.info("Operation timed out (1)")
                    if callback != "":
                        restCallback(callback, requestedOperation, blueId, blueId, "failed")
                    return
            else:
                while True:
                    ns = getSlice(free5gcMessage)
                    logger.info("NS: {}".format(ns))
                    if ns and ns.nsState.upper() == "NOT_INSTANTIATED":
                        logger.info("Removing of slice")
                        fiveTonicInterface.nsDelete(ns.id)
                        if callback != "":
                            restCallback(callback, requestedOperation, blueId, blueId, "ready")
                        return
                    else:
                        logger.info("wait {} seconds...".format(clock))
                        time.sleep(clock)
                        partialTimer += clock
                        if partialTimer == totalTime:
                            logger.info("Operation timed out (2)")
                            if callback != "":
                                restCallback(callback, requestedOperation, blueId, blueId, "failed")
                            return

    except Exception as e:
        logger.warn("Impossible to delete the slice: {}".format(e))
        if callback != "":
            restCallback(callback, requestedOperation, blueId, blueId, "failed")
        raise fastapi.HTTPException(status_code=404, detail="Impossible to delete the slice: {}".format(e))


@northRouter.post("/nfvcl/v1/api/blue/Free5GC_K8s/{blue_id}/add_slice", response_model=RestAnswer202)
async def addSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel], blue_id: str):
    onBoardObject = OnboardModel.fromFree5GcModel(free5gcMessage)
    instantiateObject = InstantiateModel.fromFree5GcModel(free5gcMessage)

    logger.info("OnboardModel instance: {}".format(onBoardObject))
    logger.info("InstantiateModel instance: {}".format(instantiateObject))

    try:
        # onboarding
        ns = fiveTonicInterface.nsOnboard(onBoardObject)
        #if ns.nsState == "NOT_INSTANTIATED":
        #    logger.warn("slice not instantiated")
        #    raise ValueError("slice not instantiated")

        #instantiate
        thread = Thread(target=instantiateSlice, args=(free5gcMessage, ns.id, instantiateObject, blue_id, "add_slice",))
        thread.start()
        return RestAnswer202()
    except Exception as e:
        logger.warn("Impossible to create the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to create the slice: {}".format(e))


@northRouter.delete("/nfvcl/v1/api/blue/Free5GC_K8s/{blue_id}/del_slice", response_model=RestAnswer202)
async def delSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel], blue_id: str):
    try:
        # get the slice from 5Tonic
        ns = getSlice(free5gcMessage)
        if not ns:
            logger.warn("Slice not found")
            raise ValueError("Slice not found")

        # terminate the slice (asynchronouns API)
        fiveTonicInterface.nsTerminate(ns.id)

        # launch a thread to check when the slice will be terminated and then delete it
        thread = Thread(target=deleteSlice, args=(free5gcMessage, blue_id, "del_slice"))
        thread.start()
        return RestAnswer202()
    except Exception as e:
        logger.warn("Impossible to delete the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to delete the slice: {}".format(e))


@northRouter.post("/nfvcl/v1/api/blue/Free5GC_K8s/{blue_id}/check_slice", response_model=RestAnswer202)
async def checkSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel], blue_id: str):
    try:
        nsLcmOpOcc = getLcmOpOcc(free5gcMessage)
        if not nsLcmOpOcc:
            raise ValueError("The nsLcmOpOcc doesn't exist")
        return RestAnswer202(description=nsLcmOpOcc.operationState, status=nsLcmOpOcc.operationState)

    except Exception as e:
        logger.warn("Impossible to check the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to check the slice: {}".format(e))





























