from LabBackend.blocks.Actions import *
from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock
from LabBackend.utils.Interfaces.IManager import IManager 
from WpfApp2.frontend.models.blocks.Blocks import Block 


class BlockManager(IManager):
    def set_link(self, ui_blocks: list[AbstractBlock], from_id: int, to_ids: list[int]):
        for main_block in ui_blocks:
            if main_block.get_id() == from_id:
                buffer = []
                for slave_id in to_ids:
                    for slave_block in ui_blocks:
                        if slave_block.get_id() == slave_id:
                            buffer.append(slave_block)
                main_block.next = buffer

    def remove_link(self, ui_blocks: list[AbstractBlock], from_id: int, to_ids: list[int]):
        for main_block in ui_blocks:
            if main_block.get_id() == from_id:
                buffer = list(main_block.next)
                buffer = [b for b in buffer if b.get_id() not in to_ids]
                main_block.next = buffer

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
            for next_block in current_block.next:
                traverse(next_block)

        traverse(start_block)
        return result

    def get_linked_frontend_blocks(self, blocks_raw_frontend: list[Block]) -> list[Block]:
        result = []
        start_block = blocks_raw_frontend[0]
        end_block = blocks_raw_frontend[1]

        if not any([start_block.next_block_id, start_block.true_block_id, start_block.false_block_id]):
            return [start_block]

        result.extend([start_block, end_block])
        remaining = [b for b in blocks_raw_frontend if b not in [start_block, end_block]]

        for block in remaining:
            if any([block.next_block_id, block.true_block_id, block.false_block_id]):
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
            if current_block.type != "if":
                next_block = next((b for b in linked_frontend_blocks if b.id == current_block.next_block_id), None)
                current_block.id = new_id
                massive.append(current_block)
                if current_block.type == "end":
                    return
                new_id += 1
                if next_block:
                    current_block.next_block_id = new_id
                    traverse(next_block)
            else:
                current_block.id = new_id
                new_id += 1
                massive.append(current_block)

                true_block = next((b for b in linked_frontend_blocks if b.id == current_block.true_block_id), None)
                false_block = next((b for b in linked_frontend_blocks if b.id == current_block.false_block_id), None)

                if current_block.true_block_id:
                    current_block.true_block_id = new_id
                    traverse(true_block)
                if current_block.false_block_id:
                    current_block.false_block_id = new_id
                    traverse(false_block)

        traverse(start_block)

        for block in massive:
            matrix[block.id] = {}
            if block.next_block_id:
                matrix[block.id][block.next_block_id] = True
            if block.true_block_id:
                matrix[block.id][block.true_block_id] = True
            if block.false_block_id:
                matrix[block.id][block.false_block_id] = True

        return matrix
