import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui

from WpfApp2.frontend.utils.managers.UIManager import UIManager
from WpfApp2.frontend.models.blocks.Blocks import Block

from LabBackend.blocks.Actions.ConstantAssignmentBlock import ConstantAssignmentBlock
from LabBackend.blocks.Actions.AssignmentBlock import AssignmentBlock
from LabBackend.blocks.Actions.PrintBlock import PrintBlock
from LabBackend.blocks.Actions.StartBlock import StartBlock
from LabBackend.utils.managers.BlockManager import BlockManager

block_counter = 1
ui_blocks = []
canvas_items = {}
connections = []
block_manager = BlockManager()
selected_block_id = None

drag_data = {
    "item": None,
    "x": 0,
    "y": 0
}

block_colors = {
    "start": "lightgreen",
    "const": "lightblue",
    "assign": "khaki",
    "print": "plum"
}

def save_canvas_as_png(canvas):
    try:
        canvas.update()
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save("diagram.png")
        messagebox.showinfo("Збережено", "Діаграму збережено як diagram.png")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти діаграму: {e}")

def create_block_ui(canvas, ui_manager, block_type, x=100, y=100):
    global block_counter

    if block_type == "start":
        backend_block = StartBlock(block_counter)
        text = "Start"
    elif block_type == "const":
        backend_block = ConstantAssignmentBlock(block_counter, "x=5")
        text = "x=5"
    elif block_type == "assign":
        backend_block = AssignmentBlock(block_counter, "y=x")
        text = "y=x"
    elif block_type == "print":
        backend_block = PrintBlock(block_counter, "y")
        text = "print(y)"
    else:
        return

    ui_blocks.append(backend_block)
    block = Block(block_id=backend_block.get_id(), block_type=block_type, text=text, position=(x, y))
    ui_manager.blocks.append(block)

    rect = canvas.create_rectangle(x, y, x + 100, y + 50,
                                   fill=block_colors.get(block_type, "gray"),
                                   tags=("block", f"id:{backend_block.get_id()}"))
    txt = canvas.create_text(x + 50, y + 25, text=text, tags=("block", f"id:{backend_block.get_id()}"))

    canvas_items[backend_block.get_id()] = {
        "block": backend_block,
        "rect": rect,
        "text": txt
    }

    block_counter += 1

def redraw_connections():
    for _, _, line in connections:
        canvas.delete(line)
    for idx, (from_id, to_id, _) in enumerate(connections):
        from_rect = canvas_items[from_id]["rect"]
        to_rect = canvas_items[to_id]["rect"]
        x1, y1 = canvas.coords(from_rect)[0:2]
        x2, y2 = canvas.coords(to_rect)[0:2]
        x1 += 50
        y1 += 25
        x2 += 50
        y2 += 25
        new_line = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
        connections[idx] = (from_id, to_id, new_line)

def on_canvas_click(event):
    global selected_block_id

    items = canvas.find_withtag(tk.CURRENT)
    if not items:
        return

    tags = canvas.gettags(items[0])
    block_id_tag = next((t for t in tags if t.startswith("id:")), None)
    if not block_id_tag:
        return

    clicked_id = int(block_id_tag.split(":")[1])
    clicked_data = canvas_items.get(clicked_id)
    clicked_block = clicked_data["block"]
    clicked_rect = clicked_data["rect"]

    if selected_block_id is None:
        selected_block_id = clicked_id
        canvas.itemconfig(clicked_rect, outline="red", width=2)
    else:
        from_data = canvas_items.get(selected_block_id)
        to_data = clicked_data
        from_block = from_data["block"]
        to_block = to_data["block"]
        from_rect = from_data["rect"]
        to_rect = to_data["rect"]

        if from_block != to_block:
            from_block.next.append(to_block)  # без hasattr

            x1, y1 = canvas.coords(from_rect)[0:2]
            x2, y2 = canvas.coords(to_rect)[0:2]
            x1 += 50
            y1 += 25
            x2 += 50
            y2 += 25
            line = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
            connections.append((selected_block_id, clicked_id, line))

        canvas.itemconfig(from_rect, outline="black", width=1)
        selected_block_id = None

def on_key_delete(event):
    global selected_block_id
    if selected_block_id is not None:
        data = canvas_items.pop(selected_block_id)
        canvas.delete(data["rect"])
        canvas.delete(data["text"])
        ui_blocks.remove(data["block"])
        for conn in [c for c in connections if selected_block_id in c[:2]]:
            canvas.delete(conn[2])
            connections.remove(conn)
        selected_block_id = None

def on_start_drag(event):
    item = canvas.find_closest(event.x, event.y)[0]
    drag_data["item"] = item
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def on_stop_drag(event):
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0
    redraw_connections()

def on_drag(event):
    if drag_data["item"]:
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(drag_data["item"], dx, dy)
        tags = canvas.gettags(drag_data["item"])
        block_id_tag = next((t for t in tags if t.startswith("id:")), None)
        if block_id_tag:
            block_id = int(block_id_tag.split(":")[1])
            for item in canvas.find_withtag("block"):
                if item != drag_data["item"] and f"id:{block_id}" in canvas.gettags(item):
                    canvas.move(item, dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y
        redraw_connections()

def run_execution(programming_language, output_box):
    if not any(block.get_name_block() == "start" for block in ui_blocks):
        messagebox.showerror("Помилка", "Не додано блок 'Start'. Будь ласка, почніть з нього.")
        return
    output_box.delete("1.0", tk.END)
    linked_blocks = block_manager.get_linked_blocks(ui_blocks)
    if not linked_blocks:
        messagebox.showwarning("Попередження", "Не знайдено зв’язків між блоками.")
        return
    for block in linked_blocks:
        import io, sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        block.execute_with_language(programming_language, amount_tabs=0)
        sys.stdout = sys.__stdout__
        output_box.insert(tk.END, captured_output.getvalue() + "\n")

def clear_all_blocks():
    global selected_block_id
    for block_id in list(canvas_items.keys()):
        data = canvas_items.pop(block_id)
        canvas.delete(data["rect"])
        canvas.delete(data["text"])
    for _, _, line in connections:
        canvas.delete(line)
    connections.clear()
    ui_blocks.clear()
    selected_block_id = None

def main():
    global canvas
    root = tk.Tk()
    root.title("Графічне програмування")
    root.geometry("1000x700")

    lang_var = tk.StringVar(value="Python")
    lang_menu = ttk.Combobox(root, textvariable=lang_var, values=["Python", "C", "C++", "Java", "C#"])
    lang_menu.pack(pady=10)

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(pady=10)

    canvas = tk.Canvas(canvas_frame, bg="white", width=900, height=500)
    canvas.pack()
    canvas.bind("<Button-1>", on_canvas_click)
    canvas.bind("<Delete>", on_key_delete)
    canvas.focus_set()

    canvas.tag_bind("block", "<ButtonPress-1>", on_start_drag)
    canvas.tag_bind("block", "<ButtonRelease-1>", on_stop_drag)
    canvas.tag_bind("block", "<B1-Motion>", on_drag)

    ui_manager = UIManager(canvas)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(root, text="🪟 Очистити все", bg="lightgray", command=clear_all_blocks).pack(pady=2)
    tk.Button(root, text="🗑 Видалити блок", bg="tomato", command=lambda: on_key_delete(None)).pack(pady=5)
    tk.Button(root, text="💾 Зберегти діаграму", bg="lightblue",
              command=lambda: save_canvas_as_png(canvas)).pack(pady=5)

    for btype, label in [("start", "Start"), ("const", "Const"), ("assign", "Assign"), ("print", "Print")]:
        tk.Button(btn_frame, text=label, command=lambda bt=btype: create_block_ui(canvas, ui_manager, bt)).pack(side=tk.LEFT, padx=5)

    tk.Button(root, text="▶️ Виконати", bg="lightgreen",
              command=lambda: run_execution(lang_var.get(), output_box)).pack(pady=10)

    output_box = tk.Text(root, height=10, width=100)
    output_box.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
