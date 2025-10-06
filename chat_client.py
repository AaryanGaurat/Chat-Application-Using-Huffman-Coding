import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from chat_system import HuffmanChatSystem
from chat_message import CompressedChatMessage
from huffman_coding import HuffmanCoder

class LiveCompressionVisualizer(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Live Huffman Compression Visualizer")
        self.geometry("600x650")
        self.configure(bg="#2b2b2b")
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.parent = parent
        
        self.results_text = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD, bg="#1e1e1e", fg="#dcdcdc", font=("Consolas", 11))
        self.results_text.pack(expand=True, fill='both', padx=10, pady=10)
        self.update_display("--- Waiting for a message ---", "System")

    def hide_window(self):
        self.withdraw()
        self.parent.on_visualizer_close()

    def update_display(self, message, sender):
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self._display_header(f"Analysis for message from: {sender}", f"'{message}'")

        if message == "--- Waiting for a message ---":
            self.results_text.config(state='disabled')
            return

        coder = HuffmanCoder()
        self._display_header("Step 1: Character Frequencies", "Count occurrences of each character.")
        self._display_table(coder.calculate_frequency(message).items(), ["Character", "Frequency"])
        
        compressed_data, huffman_codes = coder.compress(message)
        self._display_header("Step 2: Generate Huffman Codes", "Assign a unique binary code to each character.")
        self._display_table(huffman_codes.items(), ["Character", "Huffman Code"])
        
        self._display_header("Step 3: Create Compressed Message", "Replace characters with their new codes.")
        self.results_text.insert(tk.END, f"{compressed_data}\n\n")

        _, space_saved, percentage_saved = coder.get_compression_stats(message, compressed_data)
        self._display_header("Step 4: Final Results", "Compare original vs. compressed size.")
        stats = (f"Original Size      : {len(message) * 8} bits\n"
                 f"Compressed Size    : {len(compressed_data)} bits\n"
                 f"Space Saved        : {space_saved} bits ({percentage_saved:.2f}%)\n")
        self.results_text.insert(tk.END, stats)
        self.results_text.config(state='disabled')

    def _display_header(self, title, subtitle):
        self.results_text.insert(tk.END, f"--- {title.upper()} ---\n", 'header')
        self.results_text.insert(tk.END, f"{subtitle}\n\n", 'subtitle')
        self.results_text.tag_config('header', font=("Helvetica", 12, "bold"), foreground="#007acc")
        self.results_text.tag_config('subtitle', font=("Helvetica", 9, "italic"), foreground="#a0a0a0")

    def _display_table(self, data, headers):
        data = sorted(data)
        if not data: return
        col_widths = [max(len(str(item)) for item in col) for col in zip(*data, headers)]
        header_str = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        self.results_text.insert(tk.END, header_str + "\n" + "-" * len(header_str) + "\n")
        for row in data:
            self.results_text.insert(tk.END, " | ".join(f"{str(item):<{w}}" for item, w in zip(row, col_widths)) + "\n")
        self.results_text.insert(tk.END, "\n")

class GuiChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host, self.port = host, port
        self.username, self.client_socket, self.visualizer = "", None, None
        self.running = False
        self.chat_system = HuffmanChatSystem()
        
        self._setup_main_window()
        self.username = simpledialog.askstring("Username", "Please enter your username:", parent=self.window)
        
        if self.username:
            self._connect_to_server()
        else:
            self.window.destroy()

    def _setup_main_window(self):
        self.window = tk.Tk()
        self.window.title("Huffman Compressed Chat")
        self.window.geometry("500x600")
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD, bg="#2b2b2b", fg="#dcdcdc", font=("Helvetica", 10))
        self.chat_display.pack(padx=10, pady=10, expand=True, fill='both')

        input_frame = tk.Frame(self.window, bg="#1e1e1e")
        input_frame.pack(padx=10, pady=5, fill='x')

        self.message_entry = tk.Entry(input_frame, bg="#3c3c3c", fg="#dcdcdc", insertbackground="white", font=("Helvetica", 11))
        self.message_entry.bind("<Return>", self._send_message_event)
        self.message_entry.pack(side='left', expand=True, fill='x', ipady=8, padx=(0, 10))

        tk.Button(input_frame, text="Send", command=self._send_message_event, bg="#007acc", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(side='right', ipadx=10, ipady=4)
        tk.Button(input_frame, text="📊", command=self._toggle_visualizer, bg="#555555", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(side='right', padx=5)

    def _connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.running = True
            self.client_socket.send(json.dumps({'username': self.username}).encode('utf-8'))
            threading.Thread(target=self._receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
            self.window.destroy()

    def _receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if not data: break
                
                msg_data = json.loads(data)
                if 'original_text' in msg_data:
                    msg = CompressedChatMessage(msg_data['sender'], msg_data['original_text'], '', {})
                else:
                    msg = self.chat_system.decompress_message(CompressedChatMessage.from_dict(msg_data))
                
                self._update_gui_with_message(msg)
            except Exception:
                break
        if self.running: self._display_system_message("Lost connection to the server.")

    def _send_message_event(self, event=None):
        text = self.message_entry.get()
        if not text.strip(): return
        
        if self.visualizer:
            self.visualizer.update_display(text, self.username)

        try:
            compressed_msg = self.chat_system.create_message(self.username, text)
            self.client_socket.send(json.dumps(compressed_msg.to_dict()).encode('utf-8'))
            self._update_gui_with_message(compressed_msg)
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send message: {e}")

    def _update_gui_with_message(self, msg):
        if self.visualizer and msg.sender != self.username:
            self.window.after(0, self.visualizer.update_display, msg.original_text, msg.sender)
        
        self._display_message(msg)
        self.chat_system.add_to_history(msg)

    def _display_message(self, msg):
        self.chat_display.config(state='normal')
        if msg.sender == "Server":
            self.chat_display.insert(tk.END, f"--- {msg.original_text} ---\n", 'server')
        else:
            tag = msg.sender
            color = "#4ec9b0" if tag == self.username else "#9cdcfe"
            self.chat_display.tag_config(tag, foreground=color, font=("Helvetica", 10, "bold"))
            self.chat_display.insert(tk.END, f"[{msg.timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"{msg.sender}: ", tag)
            self.chat_display.insert(tk.END, f"{msg.original_text}\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)
    
    def _display_system_message(self, text):
        self._display_message(CompressedChatMessage("Server", text, '', {}))

    def _toggle_visualizer(self):
        if self.visualizer is None or not self.visualizer.winfo_exists():
            self.visualizer = LiveCompressionVisualizer(self.window)
        else:
            self.visualizer.deiconify()

    def on_visualizer_close(self):
        self.visualizer = None

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.running = False
            if self.client_socket:
                self.client_socket.close()
            self.window.destroy()

    def run(self):
        if self.username:
            self.window.mainloop()

if __name__ == "__main__":
    GuiChatClient().run()