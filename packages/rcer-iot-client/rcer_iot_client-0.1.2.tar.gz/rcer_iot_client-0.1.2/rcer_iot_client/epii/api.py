from typing import Dict

from rcer_iot_client.epii.controllers import UpdateThiesDataController
from rcer_iot_client.epii.controllers.types import UpdateThiesDataControllerInput


class EpiiAPI:
    def update_thies_data(
        self,
        ftp_port: int,
        ftp_host: str,
        ftp_password: str,
        ftp_user: str,
    ) -> Dict[str, any]:
        controller = UpdateThiesDataController(
            UpdateThiesDataControllerInput(
                ftp_port=ftp_port,
                ftp_host=ftp_host,
                ftp_password=ftp_password,
                ftp_user=ftp_user,
            )
        )
        response = controller.execute()
        return response.__dict__
