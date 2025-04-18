# -*- coding: utf-8 -*-
"""Client for the Koolnova REST API."""

import logging
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.parser import parse

from .exceptions import KoolnovaError
from .session import KoolnovaClientSession

_LOGGER = logging.getLogger(__name__)


class KoolnovaAPIRestClient:
    """Proxy to the Koolnova REST API."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API and authenticate so we can make requests.

        Args:
            username: string containing your Koolnova's app username
            password: string containing your Koolnova's app password
        """
        self.username = username
        self.password = password
        self.session: Optional[KoolnovaClientSession] = None

    def _get_session(self) -> KoolnovaClientSession:
        if self.session is None:
            self.session = KoolnovaClientSession(self.username, self.password)
        return self.session

    

   

    def get_project(self) -> Dict[str, Any]:
        
        resp = self._get_session().rest_request("GET", "projects")
        json_resp = resp.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        _LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )

        return {
            
            "Project_Name":float(json_resp["name"]),
            "Topic_Name":float(json_resp["topic"]["name"])
           
        }

    def get_project(self) -> Dict[str, Any]:
        
        resp = self._get_session().rest_request("GET", "/topics/sensors")
        json_resp = resp.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        _LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )

        return {
            "Room_Name":float(json_resp["name"]),
            "Room_id":float(json_resp["id"]),
            "Room_status" :float(json_resp["status"]),
            "Room_update_at ":float(json_resp["updated_at"]),   
            "Room_actual_temp" :float(json_resp["temperature"]),
            "Room_setpoint_temp":float(json_resp["setpoint_temperature"]),
            "Room_speed":float(json_resp["speed"])
           
        }

    