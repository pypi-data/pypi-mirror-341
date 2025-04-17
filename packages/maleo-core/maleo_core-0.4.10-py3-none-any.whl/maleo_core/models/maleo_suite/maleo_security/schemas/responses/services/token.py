from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class EncodeResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-TKN-001"
        message:str = "Succesfully encoded given payload"
        description:str = "The payload is encoded with data provided on request"
        data:MaleoSecurityTokenGeneralTransfers.Token

    class DecodeResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-TKN-002"
        message:str = "Succesfully decoded given token"
        description:str = "The token is decoded with data provided on request"
        data:MaleoSecurityTokenGeneralTransfers.Payload