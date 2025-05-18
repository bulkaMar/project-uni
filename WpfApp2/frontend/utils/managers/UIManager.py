import tkinter as tk
from tkinter import messagebox
from PIL import Image
from WpfApp2.frontend.models.blocks.Blocks import Block

class UIManager:
    def __init__(self, workspace):
        self.blocks = []
        self.source_block = None
        self.workspace_canvas = workspace

    def find_visual_child(self, parent, block):
        for item in parent.find_all():
            tags = parent.gettags(item)
            if 'block' in tags and f'id:{block.id}' in tags:
                return item
        return None

    def draw_arrow(self, from_block, to_block, arrow_color):
        from_element = self.find_visual_child(self.workspace_canvas, from_block)
        to_element = self.find_visual_child(self.workspace_canvas, to_block)

        if from_element and to_element:
            from_coords = self.workspace_canvas.coords(from_element)
            to_coords = self.workspace_canvas.coords(to_element)

            from_x = from_coords[0] + (from_coords[2] - from_coords[0]) / 2
            from_y = from_coords[1] + (from_coords[3] - from_coords[1]) / 2
            to_x = to_coords[0] + (to_coords[2] - to_coords[0]) / 2
            to_y = to_coords[1] + (to_coords[3] - to_coords[1]) / 2

            # Draw the line
            line = self.workspace_canvas.create_line(
                from_x, from_y, to_x, to_y,
                fill=arrow_color, width=2,
                arrow=tk.LAST
            )

            self.workspace_canvas.addtag_withtag(f"arrow:{from_block.id}:{to_block.id}", line)

    def get_blocks(self):
        result = []

        for block in self.blocks:
            element = self.find_visual_child(self.workspace_canvas, block)

            if element:
                coords = self.workspace_canvas.coords(element)

                block.position = (coords[0], coords[1])

            result.append(block)

        return result
