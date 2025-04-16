import httpx
import os
import importlib.util
from motto.utils import has_argument

# FIXME: A more flexible was to setup proxy?

agents_with_keys = ["ChatGPTAgent", "AnthropicAgent", 'RetrievalAgent', 'OpenRouterAgent']
class AIImporter:
    def save_errors(self, req):
        if '.' not in req:
            if importlib.util.find_spec(req) is None:
                self.errors.append(RuntimeError(f"Install {req} library to use {self.agent_name}"))
        else:
            libs = str(req).split('.')
            for lib in libs:
                if importlib.util.find_spec(lib) is None:
                    self.errors.append(RuntimeError(f"Install {req} library to use {self.agent_name}"))
                    break

    def __init__(self, agent_name, key=None, requirements=None, client_constructor=None, proxy=None, static_client=None):
        if requirements is None:
            requirements = []
        self.agent_name = agent_name
        self.errors = []
        self.requirements = requirements
        for req in self.requirements:
            self.save_errors(req)


        if agent_name in agents_with_keys:
            if key is None:
                self.errors.append(RuntimeError(f"Specify key variable for AIImporter to use {self.agent_name} agents"))
            else:
                self.key = os.environ.get(key)
                if self.key is None:
                    self.errors.append(RuntimeError(f"Specify {key} environment variable to use {self.agent_name} agents"))
        if proxy is not None:
            self.proxy = os.environ.get(proxy)
        self.client_constructor = client_constructor
        self._client = None
        self._static_client = None
        self._static_client_name = static_client

    def load_class(self, name):
        if  "." in name:
            module_name, class_name = name.rsplit(".", 1)
            parent_module = importlib.import_module(module_name)
            return getattr(parent_module, class_name)

        return importlib.import_module(name)

    def import_library(self):
        for req in self.requirements:
            importlib.import_module(req)
        if isinstance(self.client_constructor, str):
            self.client_constructor = self.load_class(self.client_constructor)
        elif isinstance(self._static_client_name, str):
            self._static_client = self.load_class(self._static_client_name)


    def has_errors(self):
        return len(self.errors) > 0

    def check_errors(self):
        if self.has_errors():
            raise self.errors[0]

    @property
    def client(self):
        if self._client is None:
            self._client = self._get_ai_client()
        return self._client

    def _get_ai_client(self):
        self.check_errors()
        self.import_library()

        if self._static_client is not None:
            return self._static_client

        if self.client_constructor is None:
            return None

        if self.proxy is not None:
            if has_argument(httpx.Client, "proxies"):
                client = self.client_constructor(http_client=httpx.Client(proxies=self.proxy))
            else:
                client = self.client_constructor(http_client=httpx.Client(proxy=self.proxy))
        else:
            client = self.client_constructor()
        return client
