"""fiveTonicRestApi

5Tonic REST API

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
import requests
from utils import create_logger
from models import *

logger = create_logger("5tonic REST interface")

class FiveTonicRestApi():
    def __init__(self, fiveTonicIP: str = None, fiveTonicPort: str = "443"):
        if not fiveTonicIP:
            raise ValueError("5Tonic server IP has a NOT valid value : IP=\"{}\"".format(fiveTonicIP))
        else:
            self.fiveTonicURL = "http://{}:{}".format(fiveTonicIP, fiveTonicPort)

        self.nsLcmURLBase = "{}/nslcm/v1".format(self.fiveTonicURL)
        self.nsInstancesURLextension = "/ns_instances"
        self.nsLCMOpOccURLExtension = "/ns_lcm_op_occs"

        self.headers = {"Content-Type": "application/json", "Version": "1.0"}

    def __checkRestResponse(self, response: requests.Response) -> bool:
        rightResponseList = [
            requests.codes.ok, requests.codes.accepted, requests.codes.created, requests.codes.no_content
        ]
        if response.status_code in rightResponseList:
            return True
        else:
            logger.error("REST API response NOT valid: URL: {} --- STATUS CODE: {} --- REASON {}".
                         format(response.url, response.status_code, response.reason))
            return False

    def __restGet(self, restUrl: str = None) -> requests.Response:
        try:
            logger.info("GET Message sent: url={} - no payload".format(restUrl))
            r = requests.get(restUrl, params=None, verify=False, stream=True, headers=self.headers)
            logger.info("GET Response received: url={} - {} - {}".format(restUrl, r, r.json()))
            return r
        except Exception as e:
            logger.error("Impossible to execute GET call: {} -- {}".format(restUrl, e))
            raise ValueError("Impossible to execute GET call: {} --- {}".format(restUrl, e))

    def __restPost(self, restUrl: str = None, data = None) -> requests.Response:
        try:
            logger.info("POST Message sent: url={} - {}".format(restUrl, data))
            r = requests.post(restUrl, json=data, params=None, verify=False, headers=self.headers)
            logger.info("POST Response received: url={} - {} - {}".format(restUrl, r, r.json()))
            return r
        except Exception as e:
            logger.error("Impossible to execute POST call: {} --- {}".format(restUrl, e))
            raise ValueError("Impossible to execute POST call: {} --- {}".format(restUrl, e))

    def __restDelete(self, restUrl: str = None, data = None) -> requests.Response:
        try:
            logger.info("DELETE Message sent: url={} - {}".format(restUrl, data))
            r = requests.delete(restUrl, json=data, params=None, verify=False, headers=self.headers)
            logger.info("DELETE Response received: url={} - {} - {}".format(restUrl, r, r.json()))
            return r
        except Exception as e:
            logger.error("Impossible to execute DELETE call: {} --- {}".format(restUrl, e))
            raise ValueError("Impossible to execute DELETE call: {} --- {}".format(restUrl, e))

    def nsOnboard(self, data: OnboardModel = None) -> NsInstance:
        """
        Execution of the onboarding process for the slice
        :return:

        """
        if not data:
            raise ValueError("data for payload is empty")
        url = "{}{}".format(self.nsLcmURLBase, self.nsInstancesURLextension)
        try:
            r = self.__restPost(restUrl=url, data=data.dict())
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
            ns = NsInstance(**r.json())
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))
        return ns

    def nsQueryList(self) -> [NsInstance]:
        """
        List of existing slices
        :return:
        """
        nsList = []
        url = "{}{}".format(self.nsLcmURLBase, self.nsInstancesURLextension)
        try:
            r = self.__restGet(restUrl=url)
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
            for item in r.json():
                nsList.append(NsInstance(**item))
            #nsList = NsInstanceList.fromArray(r.json())
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))
        #return nsList.__root__
        return nsList

    def nsQuery(self, instanceId : str = None) -> NsInstance:
        """
        Information about the specific NS
        :param instanceId:
        :return:
        """
        url = "{}{}/{}".format(self.nsLcmURLBase, self.nsInstancesURLextension, instanceId)
        if not instanceId:
            raise ValueError("the ID of the NS is not specified")
        try:
            r = self.__restGet(restUrl=url)
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
            ns = NsInstance(**r.json())
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))
        return ns

    def nsInstantiate(self, instanceId: str = None, data: InstantiateModel = None):
        """
        Instantiation of the NS
        :param instanceId:
        :param data:
        """
        if not data:
            raise ValueError("data for payload is empty")
        if not instanceId:
            raise ValueError("the ID of the NS is not specified")
        url = "{}{}/{}/instantiate".format(self.nsLcmURLBase, self.nsInstancesURLextension, instanceId)
        try:
            r = self.__restPost(restUrl=url, data=data.dict())
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))

    def nsLcmOpOccQueryList(self) -> [NsLcmOpOcc]:
        """
        LCM Operation Occurences List
        :return:
        """
        nsLcmOpOccList = []
        url = "{}{}".format(self.nsLcmURLBase, self.nsLCMOpOccURLExtension)
        try:
            r = self.__restGet(restUrl=url)
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
            #nsLcmOpOccList = NsLcmOpOccList.fromArray(r.json())
            for item in r.json():
                nsLcmOpOccList.append(NsLcmOpOcc(**item))
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))
        #return nsLcmOpOccList.__root__
        return nsLcmOpOccList

    def nsLcmOpOccQuery(self, lcmOpOccID: str = None) -> NsLcmOpOcc:
        """
        Retrieve information about the specific LCM Operation Occurence
        :param lcmOpOccID:
        :return:
        """
        url = "{}{}/{}".format(self.nsLcmURLBase, self.nsLCMOpOccURLExtension, lcmOpOccID)
        try:
            r = self.__restGet(restUrl=url)
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
            nsLcmOpOcc = NsLcmOpOcc(**r.json())
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))
        return nsLcmOpOcc

    def nsTerminate(self, instanceId: str = None):
        """
        Terminate the specific NS
        :param instanceId:
        :return:
        """
        if not instanceId:
            logger.error("ns instance ID is none")
            raise ValueError("ns instance ID is none")
        url = "{}{}/{}/terminate".format(self.nsLcmURLBase, self.nsInstancesURLextension, instanceId)
        try:
            r = self.__restPost(restUrl=url, data={})
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
        except Exception as e:
            logger.info("{}".format(e))
            raise ValueError("{}".format(e))

    def nsDelete(self, instanceId: str = None):
        """
        Remove the specific ns instance
        :param instanceId:
        :return:
        """
        if not instanceId:
            logger.error("ns instance ID is none")
            raise ValueError("ns instance ID is none")
        url = "{}{}/{}".format(self.nsLcmURLBase, self.nsInstancesURLextension, instanceId)
        try:
            r = self.__restDelete(restUrl=url, data={})
            if not self.__checkRestResponse(r):
                raise ValueError("response return this error: {}".format(r.status_code))
        except Exception as e:
            logger.error("{}".format(e))
            raise ValueError("{}".format(e))































