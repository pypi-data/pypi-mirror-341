

from mcp.types import Tool

from agentipy.tools.deploy_token import TokenDeploymentManager
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.transfer import TokenTransferManager

SOLANA_ACTIONS = {
    "GET_BALANCE": Tool(
        name="GET_BALANCE",
        description="Fetches wallet balance. input_schema Example: { token_address: 'So11111111111111111111111111111111111111112' }",
        inputSchema={
            "token_address": {
                "type": "string",
                "description": "Optional token address"
            },
        },
        handler=lambda agent, params: BalanceFetcher.get_balance(agent, params.get("token_address")),
    ),
    "TRANSFER": Tool(
        name="TRANSFER",
        description="Transfers tokens. input_schema Example: { amount: 1.5, mint: 'So11111111111111111111111111111111111111112', to: 'RecipientWalletPubkey' }",
        inputSchema={
            "amount": {
                "type": "number",
                "description": "Amount to transfer"
            },
            "mint": {
                "type": "string",
                "description": "Optional SPL token mint address"
            },
            "to": {
                "type": "string",
                "description": "Recipient wallet address"
            },
        },
        handler=lambda agent, params: TokenTransferManager.transfer(
            agent,
            params["to"],
            params["amount"],
            params.get("mint")
        ),
    ),
    "DEPLOY_TOKEN": Tool(
        name="DEPLOY_TOKEN",
        description="Deploys a new SPL token. input_schema Example: { decimals: 9 }",
        inputSchema={
            "decimals": {
                "type": "integer",
                "description": "Number of decimals"
            },
        },
        handler=lambda agent, params: TokenDeploymentManager.deploy_token(agent, params.get("decimals", 9)),
    ),
}
