

DEFAULT_LAYER1_GAS_PRICE = 20 * 10**9

HARMONY_MAINNET_URL = "https://api.harmony.one"
HARMONY_TESTNET_URL = "https://api.s0.b.hmny.io"

HARMONY_MAINNET_CHAIN_ID = 1666600000
HARMONY_TESTNET_CHAIN_ID = 1666700000

NETWORK_NAMES = ["HarmonyMainnet", "HarmonyTestnet"]
POOLS_MAP = {
    "HarmonyMainnet": {
        "chain_id": HARMONY_MAINNET_CHAIN_ID,
        "rpc_url": HARMONY_MAINNET_URL,
        "pools": [
            {
                "token_name": "VIPER",
                "pool_addr": "",
                "token_addr": "",
            }
        ]
    },
    "HarmonyTestnet": {
        "chain_id": HARMONY_TESTNET_CHAIN_ID,
        "rpc_url": HARMONY_TESTNET_URL,
        "pools": [
            {
                "token_name": "VIPER",
                "pool_addr": "0x1C4AdCaafe3da84d97B600DeA809E9A9878D49e8",
                "token_addr": "0x11F477aE5f42335928fC94601a8A81ec77b27b2b",
            }
        ]
    },
}
