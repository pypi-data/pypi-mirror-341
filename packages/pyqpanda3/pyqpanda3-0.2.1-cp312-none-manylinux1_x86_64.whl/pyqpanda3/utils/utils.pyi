class CommProtocolConfig:
    circuits_num: int
    open_error_mitigation: bool
    open_mapping: bool
    optimization_level: int
    shots: int
    def __init__(self) -> None:
        """__init__(self: utils.utils.CommProtocolConfig) -> None"""

def comm_protocol_decode(*args, **kwargs):
    """comm_protocol_decode(encode_data: bytes) -> tuple[list[QPanda3::QProg], utils.utils.CommProtocolConfig]


            @brief Decode a binary stream of a specific format into quantum computing program.
            @param[in] Encode_data: bytes.
            @return Decode result.
    """
def comm_protocol_encode(prog_list, config: CommProtocolConfig = ...) -> bytes:
    """comm_protocol_encode(prog_list: list[QPanda3::QProg], config: utils.utils.CommProtocolConfig = <utils.utils.CommProtocolConfig object at 0x7f83b20765b0>) -> bytes


            @brief Encode the quantum computing program into a binary stream of a specific format.
            @param[in] prog list:  Quantum computing program list.
            @param[in] config: Encode config.
            @return Encode result.
    """
