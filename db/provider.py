from web3 import Web3
from web3.middleware import local_filter_middleware

from singleton import Singleton
from constants import POOLS_MAP


class Web3ProviderFactory(metaclass=Singleton):
    """
    Web3ProviderFactory singleton class is used to create 
    web3 providers, signers.
    """
    def __init__(self):
        """
        Initiates the Web3ProviderFactory singleton class and creates providers for networks given in `constants`. This method is called
        when user first calls any of the other Web3ProviderFactory() methods.
        """
        self.provider_map = dict()
        for name, data in POOLS_MAP.items():
            w3_provider = Web3(Web3.HTTPProvider(data['rpc_url']))
            w3_provider.middleware_onion.add(local_filter_middleware)

            self.provider_map[name] = w3_provider

    def get_provider(self, network_name=None):
        """
        Get layer1 provider on network `network_name`.

        :param network_name: Network to connect to.
        """
        if network_name in self.provider_map:
            return self.provider_map[network_name]
        else:
            raise ValueError(f"Invalid network name {network_name}")
