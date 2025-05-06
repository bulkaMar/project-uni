from abc import ABC, abstractmethod
from typing import List, Dict
from LabBackend.Utils.Abstract import AbstractBlock
from WpfApp2.frontend.blocks import Block

class IManager(ABC):
    @abstractmethod
    def set_link(self, ui_blocks: List[AbstractBlock], from_id: int, to_id: List[int]) -> None:
        pass

    @abstractmethod
    def remove_link(self, ui_blocks: List[AbstractBlock], from_id: int, to_id: List[int]) -> None:
        pass

    @abstractmethod
    def get_linked_blocks(self, ui_blocks: List[AbstractBlock]) -> List[AbstractBlock]:
        pass

    @abstractmethod
    def get_linked_frontend_blocks(self, blocks_raw_frontend: List[Block]) -> List[Block]:
        pass

    @abstractmethod
    def get_block_by_id(self, ui_linked_blocks: List[AbstractBlock], id: int) -> AbstractBlock:
        pass

    @abstractmethod
    def create_adjacency_matrix(self, linked_frontend_blocks: List[Block]) -> Dict[int, Dict[int, bool]]:
        pass