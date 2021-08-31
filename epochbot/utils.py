def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ENDPOINT_URLS_ENUM = enum(
    MAIN='https://api.mainnet-beta.solana.com',
    DEV='https://api.devnet.solana.com',
    TEST='https://api.testnet.solana.com',
)

ENDPOINT_URLS = {
    "MAIN":'https://api.mainnet-beta.solana.com',
    "DEV":'https://api.devnet.solana.com',
    "TEST":'https://api.testnet.solana.com',
}