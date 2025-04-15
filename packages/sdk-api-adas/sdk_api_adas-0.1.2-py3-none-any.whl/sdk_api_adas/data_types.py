"""Module for event DynamoDB models."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

OrderType = Literal["desc", "asc"]
EventStateType = Literal["PENDING", "PROCESSING", "FAILED"]
EventAllStateType = Literal["SUCCESS", "PENDING", "PROCESSING", "FAILED"]
class Parameters(BaseModel):
    """Contains the parameters for the API request."""
    start: datetime
    end: datetime
    bus_plate: str | None = None
    event_type: str | None = None
    driver_id: int | None = None
    event_id: str | None = None
    vehicle_module: str | None = None
    limit: int = 4000
    order: OrderType = "desc"
    recursive: bool = True
    
class DriverInfo(BaseModel):
    """Contains information related to the driver associated with the event."""
    driverId: int  # Driver's identification (ID)
    driverName: str  # Driver's name
    similarityPrecision: float  # Precision of the similarity model
    validationThreshold: float  # Validation threshold used
    imgWidth: int | None = None  # Width of the driver's image
    imgHeight: int | None = None  # Height of the driver's image
    left: float | None = None  # Position of the top-left corner in x
    top: float | None = None  # Position of the top-left corner in y
    width: float | None = None  # Width of the driver's image
    height: float | None = None  # Height of the driver's image

class EventAnalysisDetails(BaseModel):
    """Contains information related to the ML model that evaluated the event."""
    prediction: bool  # Model's prediction
    probability: float  # Probability of the prediction
    threshold: float  # Prediction threshold
    modelName: str  # Model's name

class MediaAssets(BaseModel):
    """Contains the images and videos of the event."""

    images: list  # List of URLs pointing to the images
    videos: list  # List of URLs pointing to the videos

class ServerEventInfo(BaseModel):
    """Contains detailed information from the server."""

    vehicleId: str  # Unique identifier of the vehicle
    deviceId: str  # Unique identifier of the device or camera
    eventId: str  # Unique identifier of the event on the server
    eventStartTime: datetime  # Start date and time of the event
    eventEndTime: datetime  # End date and time of the event
    eventCreationTime: datetime  # Creation date and time of the event on the server
    alarmTypeCode: int  # Numeric code associated with the type of alarm or event
    alarmDescription: str  # Descriptive message of the alarm

class DatabaseEventBase(BaseModel):
    """Contains parameters that all database records will have."""

    pk: str | None = None  # Partition key
    sk: str | None = None  # Sort key
    busPlate: str  # Bus plate
    eventTimestamp: datetime  # Date and time when the event was generated
    contentMedia: MediaAssets  # Details related to multimedia content in S3
    vehicleModule: str  # Type of vehicle module (DCM, PCM, RCM, etc.)
    geoHash: str  # 6-digit geohash for location
    eventId: str  # Unique identifier of the event, same as ContentEventServer.eventId
    latitude: str  # Latitude of the event
    longitude: str  # Longitude of the event
    createdAt: str | None = None  # Creation date and time of the object
    timeToLive: int  # Time to live in Unix format, derived from eventTimestamp

class ServerEvent(DatabaseEventBase):
    """Contains the general information structure and additional server details, as well as the event processing state."""
    serverEventDetails: ServerEventInfo  # Details related to the event on the server
    eventState: str | None = (
        None  # Event state: "PENDING", "PROCESSING", "FAILED", or empty if already processed
    )

class ProcessedEvent(DatabaseEventBase):
    """Contains the information structure when an event has been processed."""

    driverDetails: DriverInfo  # Details related to the driver
    eventDetails: list[EventAnalysisDetails]  # List of details related to the event
    eventType: str  # Type of event, in the form {model1}#True,{model2}#False,...
    driverId: int  # Driver's identifier, same as ContentDriver.driverId
    eventState: str = (
        "SUCCESS"  # Event state: when registered in PROCESSED, the only possible state is SUCCESS
    )

    def generate_sk(self):
        """Generates the sort key."""
        return f"{self.eventTimestamp}#PROCESSED"

