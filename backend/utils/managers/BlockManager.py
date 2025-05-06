from LabBackend.Blocks.Actions import *
from LabBackend.Utils.Abstract import AbstractBlock
from LabBackend.Utils.Interfaces import IManager
from WpfApp2.frontend.blocks import Block


class BlockManager(IManager):
    def set_link(self, ui_blocks: list[AbstractBlock], from_id: int, to_ids: list[int]):
        for main_block in ui_blocks:
            if main_block.get_id() == from_id:
                buffer = []
                for slave_id in to_ids:
                    for slave_block in ui_blocks:
                        if slave_block.get_id() == slave_id:
                            buffer.append(slave_block)
                main_block.Next = buffer

    def remove_link(self, ui_blocks: list[AbstractBlock], from_id: int, to_ids: list[int]):
        for main_block in ui_blocks:
            if main_block.get_id() == from_id:
                buffer = list(main_block.Next)
                buffer = [b for b in buffer if b.get_id() not in to_ids]
                main_block.Next = buffer

    def get_linked_blocks(self, ui_blocks: list[AbstractBlock]) -> list[AbstractBlock]:
        result = []
        visited = set()
        start_block = next((b for b in ui_blocks if b.get_name_block() == "start"), None)

        if not start_block:
            return result

        def traverse(current_block):
            if not current_block or current_block.get_id() in visited:
                return
            visited.add(current_block.get_id())
            result.append(current_block)
            for next_block in current_block.Next:
                traverse(next_block)

        traverse(start_block)
        return result

    def get_linked_frontend_blocks(self, blocks_raw_frontend: list[Block]) -> list[Block]:
        result = []
        start_block = blocks_raw_frontend[0]
        end_block = blocks_raw_frontend[1]

        if not any([start_block.NextBlockId, start_block.TrueBlockId, start_block.FalseBlockId]):
            return [start_block]

        result.extend([start_block, end_block])
        remaining = [b for b in blocks_raw_frontend if b not in [start_block, end_block]]

        for block in remaining:
            if any([block.NextBlockId, block.TrueBlockId, block.FalseBlockId]):
                result.append(block)

        return result

    def get_block_by_id(self, ui_linked_blocks: list[AbstractBlock], block_id: int):
        return next((b for b in ui_linked_blocks if b.get_id() == block_id), None)

    def create_adjacency_matrix(self, linked_frontend_blocks: list[Block]) -> dict:
        matrix = {}
        massive = []
        new_id = 1
        start_block = linked_frontend_blocks[0]

        def traverse(current_block):
            nonlocal new_id
            if current_block.Type != "if":
                next_block = next((b for b in linked_frontend_blocks if b.Id == current_block.NextBlockId), None)
                current_block.Id = new_id
                massive.append(current_block)
                if current_block.Type == "end":
                    return
                new_id += 1
                if next_block:
                    current_block.NextBlockId = new_id
                    traverse(next_block)
            else:
                current_block.Id = new_id
                new_id += 1
                massive.append(current_block)

                true_block = next((b for b in linked_frontend_blocks if b.Id == current_block.TrueBlockId), None)
                false_block = next((b for b in linked_frontend_blocks if b.Id == current_block.FalseBlockId), None)

                if current_block.TrueBlockId:
                    current_block.TrueBlockId = new_id
                    traverse(true_block)
                if current_block.FalseBlockId:
                    current_block.FalseBlockId = new_id
                    traverse(false_block)

        traverse(start_block)

        for block in massive:
            matrix[block.Id] = {}
            if block.NextBlockId:
                matrix[block.Id][block.NextBlockId] = True
            if block.TrueBlockId:
                matrix[block.Id][block.TrueBlockId] = True
            if block.FalseBlockId:
                matrix[block.Id][block.FalseBlockId] = True

        return matrix