# SDK API ADAS

Este paquete es un SDK para interactuar con la API ADAS protegida por AWS IAM.

## Instalación

```bash
pip install sdk-api-adas
```

## Ejemplo de Uso

<!-- START EXAMPLE -->

```python
from sdk_api_adas.events import ApiEvents
from sdk_api_adas.utils.data_types import Parameters
from datetime import datetime, timedelta

if __name__ == "__main__":
    try:
        # Initialize the API client with your credentials
        api_client = ApiEvents(
            base_url="https://api.example.com/",
            aws_region="us-last-1",
            aws_access_key="your_access_key",
            aws_secret_key="your_access_key",
            aws_session_token="your_session_token",  # Optional
        )

        # Define the parameters for the API request
        parameters = Parameters(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
        )

        # Query: Get success events by state
        events_by_state = api_client.get_success_events_by_state(parameters)
        print("Events by state:", len(events_by_state))

        # Query: Get success events by driver
        parameters.driver_id = 123  # Set the driver ID
        events_by_driver = api_client.get_success_events_by_driver(parameters)
        print("Events by driver:", events_by_driver)

        # Query: Get success events by type
        parameters.event_type = "SPEEDING"  # Set the event type
        events_by_type = api_client.get_success_events_by_type(parameters)
        print("Events by type:", events_by_type)

        # Query: Get success events by bus
        parameters.bus_plate = "ABC123"  # Set the bus plate
        events_by_bus = api_client.get_success_events_by_bus(parameters)
        print("Events by bus:", events_by_bus)

    except Exception as e:
        print(f"An error occurred: {e}")
```

<!-- END EXAMPLE -->

## Licencia

MIT
