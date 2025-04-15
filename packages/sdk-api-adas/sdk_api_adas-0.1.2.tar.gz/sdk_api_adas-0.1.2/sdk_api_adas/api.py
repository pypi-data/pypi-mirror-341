import requests
from requests_aws4auth import AWS4Auth
from typing import Any, List


class ApiClient:
    """Cliente para interactuar con la API REST protegida por AWS IAM."""

    def __init__(
        self,
        base_url: str,
        aws_region: str,
        aws_access_key: str,
        aws_secret_key: str,
        aws_session_token: str | None = None,
    ):
        """
        Inicializa el cliente con la URL base de la API y las credenciales de AWS.

        Args:
            base_url (str): URL base de la API (e.g., "https://api.example.com").
            aws_region (str): Región de AWS (e.g., "us-east-1").
            aws_access_key (str): Clave de acceso de AWS.
            aws_secret_key (str): Clave secreta de AWS.
            aws_session_token (Optional[str]): Token de sesión de AWS (si aplica).
        """
        self.base_url = base_url
        self.aws_region = aws_region
        self.auth = AWS4Auth(
            aws_access_key,
            aws_secret_key,
            aws_region,
            "execute-api",
            session_token=aws_session_token,
        )

    def get_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str]| None = None,
    ) -> dict | List[dict]:
        """
        Realiza una solicitud GET a la API.

        Args:
            endpoint (str): El endpoint de la API al que se desea acceder.
            params (dict): Parámetros de consulta para la solicitud.
            headers (dict): Encabezados adicionales para la solicitud.

        Returns:
            dict: Respuesta de la API en formato JSON.
        """
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()
