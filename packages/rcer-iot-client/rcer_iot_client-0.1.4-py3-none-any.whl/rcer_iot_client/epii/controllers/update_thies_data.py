from http import HTTPStatus

from rcer_iot_client.epii.controllers.types.update_thies_data_types import (
    UpdateThiesDataControllerInput,
    UpdateThiesDataControllerOutput,
)
from rcer_iot_client.epii.use_cases.types import UpdateThiesDataUseCaseInput
from rcer_iot_client.epii.use_cases.update_thies_data import UpdateThiesDataUseCase
from rcer_iot_client.general_types.error_types.api.update_thies_data_error_types import (
    FetchCloudFileNamesError,
    ThiesUploadEmptyError,
)
from rcer_iot_client.general_types.error_types.common import (
    FtpClientError,
    HttpClientError,
)


class UpdateThiesDataController:
    def __init__(self, input: UpdateThiesDataControllerInput):
        self.use_case = UpdateThiesDataUseCase(
            UpdateThiesDataUseCaseInput(**input.__dict__)
        )

    async def execute(self) -> UpdateThiesDataControllerOutput:
        try:
            data = await self.use_case.execute()
            return UpdateThiesDataControllerOutput(
                message="THIES was synced successfully",
                status=HTTPStatus.OK,
                metadata={"data": data},
            )
        except (AttributeError, NameError, ValueError) as error:
            return UpdateThiesDataControllerOutput(
                message="An unexpected error occurred during use case initialization.",
                status=HTTPStatus.BAD_REQUEST,
                metadata={"error": error.__str__()},
            )
        except FtpClientError as error:
            return UpdateThiesDataControllerOutput(
                message="Ftp Client initialization fails.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                metadata={"error": error.__str__()},
            )

        except HttpClientError as error:
            return UpdateThiesDataControllerOutput(
                message="Http Client initialization fails.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                metadata={"error": error.__str__()},
            )

        except FetchCloudFileNamesError as error:
            return UpdateThiesDataControllerOutput(
                message="An error occurred while retrieving file names from the RCER cloud",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                metadata={"error": error.__str__()},
            )
        except ThiesUploadEmptyError as error:
            return UpdateThiesDataControllerOutput(
                message="No files were found to upload.",
                status=HTTPStatus.NO_CONTENT,
                metadata={"error": error.__str__()},
            )
