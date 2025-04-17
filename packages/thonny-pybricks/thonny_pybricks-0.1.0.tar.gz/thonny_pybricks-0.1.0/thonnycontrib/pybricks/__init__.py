import thonny
from pybricksdev.ble import find_device
from pybricksdev.connections.pybricks import PybricksHubBLE
from bleak.backends.winrt.util import uninitialize_sta
import asyncio
import threading
import tempfile
import os
import tkinter as tk
from tkinter import ttk

async def download_and_run():
	dialog = tk.Toplevel(thonny.get_workbench())
	dialog.geometry("500x100")
	dialog.title("Download and run")
	dialog.grab_set()
	dialog.resizable(False, False)
	dialog.attributes(toolwindow=True)
	dialog.overrideredirect(True)

	frame = ttk.Frame(dialog, borderwidth=10, relief="groove")
	frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

	labelText = tk.StringVar(value="Please wait...")
	label = ttk.Label(frame, textvariable=labelText, font=("", 20))
	label.place(relx=0.5, rely=0.5, anchor="center")

	uninitialize_sta()

	labelText.set("Finding Pybricks Hub...")
	device = await find_device()

	labelText.set("Connecting to %s..." % device.name)
	hub = PybricksHubBLE(device)
	await hub.connect()

	labelText.set("Downloading and running...")
	editor = thonny.get_workbench().get_editor_notebook().get_current_editor()
	filename = editor.get_filename()
	if filename is None:
		f = tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False)
		f.write(editor.get_content())
		f.close()
		await hub.run(f.name, wait=False)
		os.unlink(f.name)
	else:
		await hub.run(filename, wait=False)
	
	labelText.set("Disconnecting...")
	await hub.disconnect()

	dialog.destroy()

def download_action():
	def download_bg():
		asyncio.run(download_and_run())
	thread = threading.Thread(target=download_bg, daemon=True)
	thread.start()

def load_plugin():
	wb = thonny.get_workbench()
	wb.add_command(
		command_id="pybricks-download-and-run",
		menu_name="Pybricks",
		command_label="Download and run",
		handler=download_action,
		default_sequence="<F4>"
	)
