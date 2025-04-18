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
        
        response = self._get_session().rest_request("GET", "projects")
        response.raise_for_status()
        json_resp = response.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        #_LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )
        projects = []
        for project in json_resp["data"]:
            _LOGGER.debug("Project Name : %s", project["name"])
            _LOGGER.debug("Topic Name : %s", project["topic"]["name"])
            projects.append({
                "Project_Name": project["name"],
                "Topic_Name": project["topic"]["name"],
                "Mode": project["topic"]["mode"],
                "is_stop": project["topic"]["is_stop"],
                "is_online": project["topic"]["is_online"],
                "eco": project["topic"]["eco"],
                "last_sync": project["topic"]["last_sync"],


            })

        return projects

    def get_sensors(self) -> Dict[str, Any]:
        
        resp = self._get_session().rest_request("GET", "topics/sensors")
        json_resp = resp.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        #_LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )

        rooms = []
        for room in json_resp["data"]:
            _LOGGER.debug("Room Name : %s", room["name"])
            _LOGGER.debug("Room Room_actual_temp : %s", room["temperature"])
            rooms.append({
                "Room_Name": room["name"],
                "Room_id": room["id"],
                "Room_status": room["status"],
                "Room_update_at": room["updated_at"],
                "Room_actual_temp": room["temperature"],
                "Room_setpoint_temp": room["setpoint_temperature"],
                "Room_speed": room["speed"]
            })

        return rooms
    