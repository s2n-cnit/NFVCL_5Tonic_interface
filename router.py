"""Router

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
import fastapi
import time
from threading import Thread
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
from models import Free5gck8sBlueCreateModel, MiniFree5gcModel, OnboardModel, \
    InstantiateModel, NsInstance, NsLcmOpOcc
from fiveTonicRestApi import FiveTonicRestApi
from utils import create_logger

fiveTonicHost = "127.0.0.1"

logger = create_logger("Router")

northRouter = APIRouter(
    prefix="/v1",
    tags=["NorthRouter"],
    responses={404: {"description": "Not found"}}
)

fiveTonicInterface = FiveTonicRestApi(fiveTonicHost, "44300")


class RestAnswer202(BaseModel):
    #id: str
    description: str = "operation submitted"
    status: str = "submitted"


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


def deleteSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]):
    # check if slice is terminated and then delete it
    partialTimer = 0
    totalTime = 600 # 5 minutes in seconds
    clock = 2 # in seconds
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
                    logger.info("Operation timed out")
                    break
                continue
            else:
                logger.info("Removing of slice")
                fiveTonicInterface.nsDelete(getSlice(free5gcMessage).id)
                break
    except Exception as e:
        logger.warn("Impossible to delete the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to delete the slice: {}".format(e))


@northRouter.post("/addslice", response_model=RestAnswer202)
async def addSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]):
    onBoardObject = OnboardModel.fromFree5GcModel(free5gcMessage)
    instantiateObject = InstantiateModel.fromFree5GcModel(free5gcMessage)

    logger.info("OnboardModel instance: {}".format(onBoardObject))
    logger.info("InstantiateModel instance: {}".format(instantiateObject))

    try:
        # onboarding
        ns = fiveTonicInterface.nsOnboard(onBoardObject)
        if ns.nsState == "NOT_INSTANTIATED":
            logger.warn("slice not instantiated")
            raise ValueError("slice not instantiated")

        #instantiate
        fiveTonicInterface.nsInstantiate(ns.id, instantiateObject)
    except Exception as e:
        logger.warn("Impossible to create the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to create the slice: {}".format(e))

    return RestAnswer202()


@northRouter.post("/delslice", response_model=RestAnswer202)
async def delSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]):
    try:
        # get the slice from 5Tonic
        ns = getSlice(free5gcMessage)
        if not ns:
            logger.warn("Slice not found")
            raise ValueError("Slice not found")

        # terminate the slice (asynchronouns API)
        fiveTonicInterface.nsTerminate(ns.id)

        # launch a thread to check when the slice will be terminated and then delete it
        thread = Thread(target=deleteSlice, args=(free5gcMessage,))
        thread.start()
        return RestAnswer202()
    except Exception as e:
        logger.warn("Impossible to delete the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to delete the slice: {}".format(e))


@northRouter.post("/checkslice", response_model=RestAnswer202)
async def checkSlice(free5gcMessage: Union[Free5gck8sBlueCreateModel, MiniFree5gcModel]):
    try:
        nsLcmOpOcc = getLcmOpOcc(free5gcMessage)
        if not nsLcmOpOcc:
            raise ValueError("The nsLcmOpOcc doesn't exist")
        return RestAnswer202(description=nsLcmOpOcc.operationState, status=nsLcmOpOcc.operationState)

    except Exception as e:
        logger.warn("Impossible to check the slice: {}".format(e))
        raise fastapi.HTTPException(status_code=404, detail="Impossible to check the slice: {}".format(e))





























