from datetime import datetime, timedelta
from .utils.api import ApiClient
from typing import List
from pydantic import BaseModel
from .utils.data_types import Parameters


class ApiEvents(ApiClient):
    """Cliente para interactuar con la API REST protegida por AWS IAM."""

    def __init__(
        self,
        base_url: str,
        aws_region: str,
        aws_access_key: str,
        aws_secret_key: str,
        aws_session_token: str | None = None,
    ):
        super().__init__(
            base_url,
            aws_region,
            aws_access_key,
            aws_secret_key,
            aws_session_token,
        )
    
    def _fetch_all_data_recursively(self, endpoint: str, parameters: Parameters, response: List[dict]) -> List[dict]:
        """
        Fetches all data recursively for a given endpoint and parameters.

        Args:
            endpoint (str): API endpoint to call.
            parameters (Parameters): Parameters for the API request.
            response (List[dict]): Current accumulated response.

        Returns:
            List[dict]: Complete list of data fetched recursively.
        """
        if len(response) < parameters.limit:  # Default limit is 4000
            return response
        else:
            # Adjust the date range for the next recursive call
            if parameters.order == "desc":
                new_end = datetime.fromisoformat(response[-1]["eventTimestamp"])
                next_parameters = parameters.model_copy(update={"end": new_end})
            else:  # order == "asc"
                new_start = datetime.fromisoformat(response[-1]["eventTimestamp"])
                next_parameters = parameters.model_copy(update={"start": new_start})

            # Recursive call to fetch additional data
            additional_response = self.get_request(
                endpoint=endpoint,
                params={
                    "start": next_parameters.start.isoformat(),
                    "end": next_parameters.end.isoformat(),
                    "busPlate": next_parameters.bus_plate,
                    "driverId": next_parameters.driver_id,
                    "eventId": next_parameters.event_id,
                    "vehicleModule": next_parameters.vehicle_module,
                    "limit": next_parameters.limit,
                    "order": next_parameters.order,
                },
            )
            if not isinstance(additional_response, list):
                raise ValueError(f"Unexpected response format: {additional_response}")

            return response + self._fetch_all_data_recursively(endpoint, next_parameters, additional_response)

    def get_success_events_by_state(self, parameters: Parameters) -> List[dict]:
        """
        Obtiene eventos exitosos por estado.

        Args:
            params (Parameters): Objeto con los parámetros comunes.

        Returns:
            List[dict]: Lista de eventos procesados.

        Raises:
            ValueError: Si la respuesta no es válida o contiene un error.
        """
        try:
            response = self.get_request(
                endpoint=f"events/SUCCESS/by-state",
                params={
                    "start": parameters.start.isoformat(),
                    "end": parameters.end.isoformat(),
                    "busPlate": parameters.bus_plate,
                    "driverId": parameters.driver_id,
                    "eventId": parameters.event_id,
                    "vehicleModule": parameters.vehicle_module,
                    "limit": parameters.limit,
                    "order": parameters.order,
                },
            )
            if not isinstance(response, list):
                raise ValueError(f"Unexpected response format: {response}")

            # Use recursive logic if enabled
            if parameters.recursive:
                return self._fetch_all_data_recursively("events/SUCCESS/by-state", parameters, response)
            return response
        except Exception as e:
            raise ValueError(f"Failed to fetch success events by state: {e}")


    def get_success_events_by_driver(
        self,
        parameters: Parameters,
    ) -> List[dict]:
        """
        Obtiene eventos exitosos por conductor.

        Args:
            parameters (Parameters): Parametros de la consulta.

        Returns:
            List[dict]: Lista de eventos procesados.
        """
        try:
            if(parameters.driver_id is None):
                raise ValueError("El parámetro 'driver_id' no puede ser None")
            response = self.get_request(
                endpoint=f"events/SUCCESS/by-driver/{parameters.driver_id}",
                params={
                    "start": parameters.start.isoformat(),
                    "end": parameters.end.isoformat(),
                    "busPlate": parameters.bus_plate,
                    "driverId": parameters.driver_id,
                    "eventId": parameters.event_id,
                    "vehicleModule": parameters.vehicle_module,
                    "limit": parameters.limit,
                    "order": parameters.order,
                },
            )
            if not isinstance(response, list):
                raise ValueError(f"Unexpected response format: {response}")

            # Use recursive logic if enabled
            if parameters.recursive:
                return self._fetch_all_data_recursively("events/SUCCESS/by-state", parameters, response)
            return response
        except Exception as e:
            raise ValueError(f"Failed to fetch success events by state: {e}")

    def get_success_events_by_type(
        self,
        parameters: Parameters,
    ) -> List[dict]:
        """
        Obtiene eventos exitosos por tipo.

        Args:
            parameters (Parameters): Parametros de consulta.

        Returns:
            List[dict]: Lista de eventos procesados.
        """
        try:
            if(parameters.event_type is None):
                raise ValueError("El parámetro 'event_type' no puede ser None")
            response = self.get_request(
                endpoint=f"events/SUCCESS/by-type/{parameters.event_type}",
                params={
                    "start": parameters.start.isoformat(),
                    "end": parameters.end.isoformat(),
                    "busPlate": parameters.bus_plate,
                    "driverId": parameters.driver_id,
                    "eventId": parameters.event_id,
                    "vehicleModule": parameters.vehicle_module,
                    "limit": parameters.limit,
                    "order": parameters.order,
                },
            )
            if not isinstance(response, list):
                raise ValueError(f"Unexpected response format: {response}")

            # Use recursive logic if enabled
            if parameters.recursive:
                return self._fetch_all_data_recursively("events/SUCCESS/by-state", parameters, response)
            return response
        except Exception as e:
            raise ValueError(f"Failed to fetch success events by state: {e}")

    def get_success_events_by_bus(
        self, parameters: Parameters
    ) -> List[dict]:
        """
        Obtiene eventos exitosos por bus.

        Args:                        
            params (Parameters): Objeto con los parámetros comunes.

        Returns:
            List[dict]: Lista de eventos procesados.
        """
        try:
            if(parameters.bus_plate is None):
                raise ValueError("El parámetro 'bus_plate' no puede ser None")
            response = self.get_request(
                endpoint=f"events/SUCCESS/by-bus/{parameters.bus_plate}",
                params={
                    "start": parameters.start.isoformat(),
                    "end": parameters.end.isoformat(),
                    "busPlate": parameters.bus_plate,
                    "driverId": parameters.driver_id,
                    "eventId": parameters.event_id,
                    "vehicleModule": parameters.vehicle_module,
                    "limit": parameters.limit,
                    "order": parameters.order,
                },
            )
            if not isinstance(response, list):
                raise ValueError(f"Unexpected response format: {response}")

            # Use recursive logic if enabled
            if parameters.recursive:
                return self._fetch_all_data_recursively("events/SUCCESS/by-state", parameters, response)
            return response
        except Exception as e:
            raise ValueError(f"Failed to fetch success events by state: {e}")

