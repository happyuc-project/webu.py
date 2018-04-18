from webu.providers import (
    BaseProvider,
)

from .middleware import (
    default_transaction_fields_middleware,
    happyuc_tester_fixture_middleware,
    happyuc_tester_middleware,
)


class HappyUCTesterProvider(BaseProvider):
    middlewares = [
        default_transaction_fields_middleware,
        happyuc_tester_fixture_middleware,
        happyuc_tester_middleware,
    ]
    happyuc_tester = None
    api_endpoints = None

    def __init__(self, happyuc_tester=None, api_endpoints=None):
        if happyuc_tester is None:
            # do not import eth_tester until runtime, it is not a default dependency
            from eth_tester import HappyUCTester
            self.happyuc_tester = HappyUCTester()
        else:
            self.happyuc_tester = happyuc_tester

        if api_endpoints is None:
            # do not import eth_tester derivatives until runtime, it is not a default dependency
            from .defaults import API_ENDPOINTS
            self.api_endpoints = API_ENDPOINTS
        else:
            self.api_endpoints = api_endpoints

    def make_request(self, method, params):
        namespace, _, endpoint = method.partition('_')
        try:
            delegator = self.api_endpoints[namespace][endpoint]
        except KeyError:
            return {
                "error": "Unknown RPC Endpoint: {0}".format(method),
            }

        try:
            response = delegator(self.happyuc_tester, params)
        except NotImplementedError:
            return {
                "error": "RPC Endpoint has not been implemented: {0}".format(method),
            }
        else:
            return {
                'result': response,
            }

    def isConnected(self):
        return True
