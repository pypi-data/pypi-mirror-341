from .manager import MaleoSOAPIEHTTPClientManager
from .controllers import MaleoSOAPIEHTTPControllers
from .services import MaleoSOAPIEHTTPServices

class MaleoSOAPIEHTTPClient:
    Manager = MaleoSOAPIEHTTPClientManager
    Controllers = MaleoSOAPIEHTTPControllers
    Services = MaleoSOAPIEHTTPServices