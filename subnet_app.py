#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

class OctetFrame(tk.Frame):
    def __init__(self, parent, octet_index, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.octet_index = octet_index
        self.bits = [0] * 8
        self.buttons = []
        self.bit_labels = []
        self.bit_values = [128, 64, 32, 16, 8, 4, 2, 1]
        self.create_widgets()

    def create_widgets(self):
        # Label for Octet Number
        tk.Label(self, text=f"Octet {self.octet_index + 1}", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=8, pady=(0, 5))

        # Create labels for bit positions (Bit 1 to Bit 8)
        for i in range(8):
            lbl = tk.Label(self, text=f"Bit {i + 1}")
            lbl.grid(row=1, column=i, padx=5)

        # Create 8 buttons for each bit
        for i in range(8):
            btn = tk.Button(self, text='0', width=4, command=lambda i=i: self.toggle_bit(i))
            btn.grid(row=2, column=i, padx=5)
            self.buttons.append(btn)

        # Create labels for bit values (128 to 1)
        for i in range(8):
            lbl = tk.Label(self, text=str(self.bit_values[i]))
            lbl.grid(row=3, column=i, padx=5)
            self.bit_labels.append(lbl)

    def toggle_bit(self, index):
        self.bits[index] = 1 - self.bits[index]
        self.update_bit_display(index)
        self.parent.update_full_ip_display()

    def update_bit_display(self, index):
        bit_state = self.bits[index]
        self.buttons[index].config(text=str(bit_state), fg='red' if bit_state == 1 else 'black')
        self.bit_labels[index].config(fg='red' if bit_state == 1 else 'black')

    def reset_bits(self):
        self.bits = [0] * 8
        for i in range(8):
            self.update_bit_display(i)

    def get_decimal_value(self):
        return sum(bit * value for bit, value in zip(self.bits, self.bit_values))

    def get_binary_string(self):
        return ''.join(str(bit) for bit in self.bits)

class SubnettingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Subnetting Educational Tool")
        self.octet_frames = []
        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Header Frame for Example IP Address
        header_frame = tk.Frame(self)
        header_frame.pack(pady=10)

        example_ip = "192.168.1.0"
        octets = example_ip.split('.')

        # Display Example IP Address with Octet Labels
        tk.Label(header_frame, text="Example IP Address:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=7, pady=(0, 5))
        for i, octet in enumerate(octets):
            tk.Label(header_frame, text=f"Octet {i + 1}\n{octet}", font=("Helvetica", 10), padx=5).grid(row=1, column=2*i)
            if i < len(octets) - 1:
                tk.Label(header_frame, text=".", font=("Helvetica", 10)).grid(row=1, column=2*i + 1, pady=(18, 0))

        # Separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=5)

        # Frame for all octets
        self.octets_frame = tk.Frame(self)
        self.octets_frame.pack(pady=10)

        # Create four OctetFrames stacked vertically
        for i in range(4):
            frame = OctetFrame(self, i, bd=2, relief="groove")
            frame.pack(pady=5, fill='x', expand=True)
            self.octet_frames.append(frame)

        # Label to display the full IP address
        self.full_ip_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.full_ip_label.pack(pady=10)

        # Add the Clear button
        clear_button = tk.Button(self, text='Clear', command=self.clear_all_bits)
        clear_button.pack(pady=10)

        # Initialize the display
        self.update_full_ip_display()

    def update_full_ip_display(self):
        decimal_values = [frame.get_decimal_value() for frame in self.octet_frames]
        binary_strings = [frame.get_binary_string() for frame in self.octet_frames]
        full_ip_decimal = '.'.join(map(str, decimal_values))
        full_ip_binary = '.'.join(binary_strings)
        self.full_ip_label.config(text=f"Binary: {full_ip_binary}\nDecimal: {full_ip_decimal}")

    def clear_all_bits(self):
        for frame in self.octet_frames:
            frame.reset_bits()
        self.update_full_ip_display()

    def on_resize(self, event):
        # Adjust font size based on window width
        new_size = max(10, int(event.width / 50))
        for frame in self.octet_frames:
            for btn in frame.buttons:
                btn.config(font=("Helvetica", new_size))
            for lbl in frame.bit_labels:
                lbl.config(font=("Helvetica", new_size))
        self.full_ip_label.config(font=("Helvetica", new_size + 6))

if __name__ == "__main__":
    app = SubnettingApp()
    app.mainloop()

