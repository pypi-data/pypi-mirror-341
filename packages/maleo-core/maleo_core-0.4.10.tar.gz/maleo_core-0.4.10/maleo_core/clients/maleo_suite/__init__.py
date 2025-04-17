from .maleo_shared import MaleoSharedClients
from .maleo_security import MaleoSecurityClients
from .maleo_access import MaleoAccessClients
from .maleo_soapie import MaleoSOAPIEClients

class MaleoSuiteClients:
    MaleoShared = MaleoSharedClients
    MaleoSecurity = MaleoSecurityClients
    MaleoAccess = MaleoAccessClients
    MaleoSOAPIE = MaleoSOAPIEClients