"""
Mimir: A reusable UI controller for tkinter/ttkbootstrap
"""

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as msg
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


class Mimir:
    def __init__(self, app):
        self.app = app
        self.currentView = None
        self.invalidEntries = set()
        self._validatorResolver = lambda name: None  # Placeholder
        self.fieldRenderers = {
            "entry": self._renderEntryField,
            "combobox": self._renderComboboxField,
            "heading": self._renderHeading,
        }

    def setValidatorResolver(self, resolverFunc):
        self._validatorResolver = resolverFunc

    def switchView(self, newFrameFunc, gridOptions=None, **kwargs):
        if self.currentView:
            self.currentView.destroy()

        container = tb.Frame(self.app)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        topBar = tb.Frame(container)
        topBar.grid(row=0, column=0, sticky="ew")
        newFrame = newFrameFunc(self, **kwargs)

        options = gridOptions or {"row": 1, "column": 0, "sticky": "n", "padx": 50, "pady": 20}
        newFrame.grid(**options)
        self.app.rowconfigure(options.get("row", 0), weight=1)
        self.app.columnconfigure(options.get("column", 0), weight=1)
        self.currentView = newFrame
        self.app.update_idletasks()
        self.app.geometry("")
        return newFrame

    def popupView(self, viewFunc, title="Popup", size="fit", width=500, height=400, modal=False):
        popup = tk.Toplevel(self.app)
        popup.title(title)
        popup.transient(self.app)
        popup.resizable(False, False)

        if size == "fit":
            popup.update_idletasks()
            popup.geometry("")
        else:
            popup.geometry(f"{width}x{height}")

        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
        viewFrame = viewFunc(self, popup)
        viewFrame.grid(row=0, column=0, sticky="nsew")

        if modal:
            popup.grab_set()
            popup.focus_set()

        return popup

    def addTooltip(self, widget, text):
        ToolTip(widget, text, bootstyle=(SECONDARY, INVERSE))

    def renderFields(self, parent, fields, startRow=0):
        row = startRow
        for field in fields:
            field_type = field.get("type", "entry")
            renderer = self.fieldRenderers.get(field_type)
            if renderer:
                renderer(parent, row, field)
                row += 2 if field_type != "heading" else 1
        return row

    def _renderEntryField(self, parent, row, field):
        tb.Label(parent, text=field["label"]).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = tb.Entry(parent, textvariable=field["variable"], width=field.get("width", 20))
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        if field.get("tooltip"):
            self.addTooltip(entry, field["tooltip"])
        self._setupValidation(entry, field.get("validation"))

    def _renderComboboxField(self, parent, row, field):
        tb.Label(parent, text=field["label"]).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        combo = tb.Combobox(parent, textvariable=field["variable"], values=field["values"], state="readonly")
        combo.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        if field.get("tooltip"):
            self.addTooltip(combo, field["tooltip"])

    def _renderHeading(self, parent, row, field):
        font = self.getCurrentFont()
        font.configure(weight="bold")
        tb.Label(parent, text=field["label"], font=font).grid(
            row=row, column=0, columnspan=2, pady=(10, 5), sticky="w"
        )

    def _setupValidation(self, widget, validationName):
        fn = self._validatorResolver(validationName) if validationName else None
        if not callable(fn):
            return

        def validate(event):
            if fn(widget.get()):
                self.clearInvalid(widget)
            else:
                self.markInvalid(widget)

        widget.bind("<FocusOut>", validate)

    def markInvalid(self, widget):
        widget.config(bootstyle="danger")
        self.invalidEntries.add(widget)

    def clearInvalid(self, widget):
        widget.config(bootstyle="none")
        self.invalidEntries.discard(widget)

    def addNextButton(self, parent, row, command, label="Next", tooltip=None):
        def wrapped():
            if self.invalidEntries:
                msg.showerror("Error", "Some fields are invalid.")
                return
            command()

        btn = tb.Button(parent, text=label, command=wrapped, bootstyle="success")
        btn.grid(row=row, column=0, columnspan=2, pady=(10, 5))
        if tooltip:
            self.addTooltip(btn, tooltip)
        return btn

    def getCurrentFont(self):
        style = tb.Style()
        fontName = style.lookup("TLabel", "font")
        return tkFont.Font(font=fontName)

    def registerFieldType(self, name, renderer):
        self.fieldRenderers[name] = renderer

    def unregisterFieldType(self, name):
        self.fieldRenderers.pop(name, None)

    def clearInvalidEntries(self):
        for widget in list(self.invalidEntries):
            self.clearInvalid(widget)

    def resetView(self):
        if self.currentView:
            self.currentView.destroy()
        self.currentView = None