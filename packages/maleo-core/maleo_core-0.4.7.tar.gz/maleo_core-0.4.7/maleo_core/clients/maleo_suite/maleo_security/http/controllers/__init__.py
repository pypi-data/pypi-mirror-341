from .secret import MaleoSecuritySecretHTTPController
from .key import MaleoSecurityKeyHTTPController
from .encryption import MaleoSecurityEncryptionHTTPController
from .hash import MaleoSecurityHashHTTPController
from .token import MaleoSecurityTokenHTTPController

class MaleoSecurityHTTPControllers:
    Secret = MaleoSecuritySecretHTTPController
    Key = MaleoSecurityKeyHTTPController
    Encryption = MaleoSecurityEncryptionHTTPController
    Hash = MaleoSecurityHashHTTPController
    Token = MaleoSecurityTokenHTTPController