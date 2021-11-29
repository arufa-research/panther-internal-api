

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
                "pool_addr": "0xaCF4E7ff53e4b89B521160Ecf201cE5B1D41a6B4",
                "token_addr": "0xea589e93ff18b1a1f1e9bac7ef3e86ab62addc79",
            },
            {
                "token_name": "JEWEL",
                "pool_addr": "0xd69376EB161d3F33597d34B9A4F88231BDbd92b2",
                "token_addr": "0x72cb10c6bfa5624dd07ef608027e366bd690048f",
            },
            {
                "token_name": "USDT",
                "pool_addr": "0xB6b6094dc5772F3C1A3fb73364758DD1d303FA0e",
                "token_addr": "0x3c2b8be99c50593081eaa2a724f0b8285f5aba8f",
            }
        ]
    },
    "HarmonyTestnet": {
        "chain_id": HARMONY_TESTNET_CHAIN_ID,
        "rpc_url": HARMONY_TESTNET_URL,
        "pools": [
            {
                "token_name": "VIPER-0",
                "pool_addr": "0x94892f24CCb63fe44eedAB8316A91b20698620Db",
                "token_addr": "0x11F477aE5f42335928fC94601a8A81ec77b27b2b",
            },
            {
                "token_name": "VIPER-1",
                "pool_addr": "0x1C4AdCaafe3da84d97B600DeA809E9A9878D49e8",
                "token_addr": "0x11F477aE5f42335928fC94601a8A81ec77b27b2b",
            }
        ]
    },
}
