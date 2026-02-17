import datetime
from sbc_package.essential_files.essentials import Chain

class BlockChain():
    running: bool
    connection_established: bool
    external_ip: str
    chain: Chain
    sharing_files: list

    def __init__(self):
        """
        Initializes your blockchain,
        fetches external and local ip
        """
        pass

    def create(self) -> None:
        """
        creates server that serves the purpose of
        only sending packages to devises to reconnect
        them in a 'ring'
        :return:
        """

    def join(self) -> None:
        """
        connects you to any blockchain you want,
        gets instructions and processes them, starts
        sharing files when done
        :return:
        """

    def get_local_ip(self) -> str:
        """
        returns you your ip in LAN

        (don't really know how this stuff work, but ok)
        :return:
        """


class BlockChainProtocol():
    """
    Different prefixes for sending instructions
    """
    pass
