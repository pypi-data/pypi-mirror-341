"""Get block number tool for EVM RPC plugin."""

from pydantic import BaseModel, Field
from web3 import Web3

from lomen.plugins.base import BaseTool


class GetBlockNumberParams(BaseModel):
    rpc_url: str = Field(..., description="The RPC URL for the blockchain")
    chain_id: int = Field(..., description="The chain ID for the blockchain")


class GetBlockNumber(BaseTool):
    """
    Fetch the current block number from the specified EVM blockchain.
    """

    name = "get_block_number"

    # Remove the synchronous run method or make it raise NotImplementedError
    # def run(self, *args, **kwargs):
    #     raise NotImplementedError("Use the asynchronous 'arun' method.")

    async def arun(self, rpc_url: str, chain_id: int):
        """
        Asynchronously fetch the current block number from the specified EVM blockchain.
        (Note: Internally uses synchronous web3 calls)

        Args:
            rpc_url: The RPC URL for the blockchain
            chain_id: The chain ID for the blockchain

        Returns:
            Dictionary containing the block number
        """
        # This logic remains synchronous as web3 is sync
        try:
            # Get a Web3 instance for the specified RPC URL and chain ID
            web3 = Web3(Web3.HTTPProvider(rpc_url))

            # Get the current block number
            block_number = web3.eth.block_number

            return {
                "block_number": block_number,
            }
        except Exception as e:
            # Wrap synchronous exceptions if needed, though direct raise is often fine
            raise Exception(f"Failed to get block number: {str(e)}")

    def get_params(self):
        return GetBlockNumberParams
