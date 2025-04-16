"""
Abstract Mimir (updated): Reusable UI controller with abstract block rendering
"""

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as msg
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

from jabs_mimir.DataBlockWrapper import DataBlockWrapper


class Mimir:
    widthEntry = 20
    widthCombo = widthEntry - 2

    def __init__(self, app):
        """
        Initialize Mimir with reference to the root app window.
        """
        self.app = app
        self.currentView = None
        self.invalidEntries = set()
        self._validatorResolver = lambda name: None
        self.fieldRenderers = {
            "entry": self._renderEntryField,
            "combobox": self._renderComboboxField,
            "heading": self._renderHeading,
        }
        self._allowThemeToggle = False

    def allowDarkMode(self, enabled=True):
        """Enable or disable theme toggle button in the top right."""
        self._allowThemeToggle = enabled

    def _toggleTheme(self):
        """Switch between light and dark themes."""
        current = self.app.style.theme.name
        self.app.style.theme_use("darkly" if current != "darkly" else "cosmo")

    def setValidatorResolver(self, resolverFunc):
        """Register a function that returns validation callbacks by name."""
        self._validatorResolver = resolverFunc

    def switchView(self, newFrameFunc, gridOptions=None, **kwargs):
        """
        Replace the current view with a new frame built by newFrameFunc.
        Automatically configures geometry and grid placement.
        """        
        if self.currentView:
            self.currentView.destroy()

        container = tb.Frame(self.app)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        topBar = tb.Frame(container)
        topBar.grid(row=0, column=0, sticky="ew")

        if self._allowThemeToggle:
            tb.Button(topBar, text="Theme", command=self._toggleTheme).pack(side="right", padx=10, pady=10)

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
        """
        Open a popup window and embed a view frame into it.
        If `modal=True`, interaction with other windows is blocked.
        """        
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

    def renderBlockUI(self, container, fields, blockList, layout="horizontal", meta=None, label=None, noRemove=False):
        """
        Render a labeled input block with specified fields and layout style.
        Automatically attaches the block to blockList and handles UI labels and deletion logic.
        """        
        index = len(blockList) + 1
        labelText = label or f"Block {index}"
        frame = tb.LabelFrame(container, text=labelText)
        frame.configure(labelanchor="n") 
        
        if layout == "vertical":
            frame.grid(row=index - 1, column=0, padx=10, pady=10, sticky="w")
        else:
            frame.grid(row=0, column=index - 1, padx=10, pady=10, sticky="n")

        boldFont = self.getCurrentFont()
        boldFont.configure(weight="bold")

        if meta is None:
            meta = {}
        if "custom_label" not in meta and label:
            meta["custom_label"] = label

        blockMeta = {
            "frame": frame,
            "fields": fields,
            "fields_by_key": {f["key"]: f["variable"] for f in fields if "key" in f},
            "layout": layout,
            **meta
        }


        wrapper = DataBlockWrapper(blockMeta)
        blockList.append(wrapper)

        row = 0
        for field in fields:
            ftype = field.get("type", "entry")
            renderer = self.fieldRenderers.get(ftype)
            if renderer:
                renderer(frame, row, field)

                # Adjust row offset based on field type
                if ftype == "fileupload":
                    row += 3
                elif ftype == "heading":
                    row += 1
                else:
                    row += 2

        if not noRemove:
            removeBtn = tb.Button(
                frame,
                text="🗑️ Ta bort",
                bootstyle="danger-outline",
                command=lambda w=wrapper: self.removeBlock(blockList, w)
            )
            removeBtn.grid(row=row, column=0, columnspan=2, pady=(10, 5))

        return wrapper


    def registerFieldType(self, name, renderer):
        """Register a custom field renderer by name."""        
        self.fieldRenderers[name] = renderer

    def _renderEntryField(self, parent, row, field):
        """Internal: Render an entry field with label."""
        self.addLabeledEntry(
            parent=parent,
            row=row,
            label=field["label"],
            variable=field["variable"],
            validation=field.get("validation"),
            **field.get("options", {})  # <-- wildcard pass-through
        )

    def _renderComboboxField(self, parent, row, field):
        """Internal: Render a combobox field with label."""
        self.addLabeledCombobox(
            parent=parent,
            row=row,
            label=field["label"],
            variable=field["variable"],
            values=field["values"],
            **field.get("options", {})  # <-- pass all UI customization
        )
    def _renderHeading(self, parent, row, field):
        """Internal: Render a bold heading label within a form."""
        font = self.getCurrentFont()
        font.configure(weight="bold")

        align = field.get("options", {}).get("align", "w")  # default to left

        tb.Label(
            parent,
            text=field["label"],
            font=font
        ).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky=align)


    def _setupValidation(self, widget, validationName):
        """Bind focus-out validation using a named validation function."""
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
        """Mark a widget as invalid with red border styling."""
        widget.config(bootstyle="danger")
        self.invalidEntries.add(widget)

    def clearInvalid(self, widget):
        """Clear error styling from a widget."""
        widget.config(bootstyle="none")
        self.invalidEntries.discard(widget)

    def addNextButton(self, parent, row, command, label="Nästa", tooltip=None, column=None, columnspan=None):
        """
        Add a 'Next' button to the given row. Automatically spans the full width
        of horizontal blocks if no column or columnspan is provided.
        Blocks execution if any fields are invalid.
        """        
        def wrapped():
            if self.invalidEntries:
                msg.showerror("Fel", "Alla fält måste vara giltiga innan du kan fortsätta.")
                return
            command()

        # Calculate default columnspan if not explicitly provided
        if column is None or columnspan is None:
            # Find all unique columns used in row=0 (block layout)
            used_columns = set()
            for child in parent.winfo_children():
                grid = child.grid_info()
                if grid.get("row") == 0 and "column" in grid:
                    used_columns.add(int(grid["column"]))

            if not used_columns:
                column = 0
                columnspan = 1
            else:
                column = 0
                columnspan = max(used_columns) + 1

        btn = tb.Button(parent, text=label, command=wrapped, bootstyle="success")
        btn.grid(row=row, column=column, columnspan=columnspan, pady=(10, 5))

        if tooltip:
            self.addTooltip(btn, tooltip)

        return btn


    def getCurrentFont(self):
        """Return the default font currently used by ttkbootstrap widgets."""
        style = tb.Style()
        fontName = style.lookup("TLabel", "font")
        return tkFont.Font(font=fontName)

    def addTooltip(self, widget, text):
        """Attach a styled tooltip to a widget."""
        ToolTip(widget, text, bootstyle=(SECONDARY, INVERSE))

    def removeBlock(self, blockList, wrapper):
        """
        Remove a UI block from view and list. Automatically reindexes
        and repositions remaining blocks.
        """        
        frame = wrapper.meta.get("frame")
        layout = wrapper.meta.get("layout", "horizontal")
        if frame:
            frame.destroy()
        blockList.remove(wrapper)

        for i, block in enumerate(blockList):
            frame = block.meta["frame"]
            new_label = f"Butik {i + 1}"

            # Update visual label
            frame.config(text=new_label)

            # Update meta so future logic knows the new label/index
            block.meta["custom_label"] = new_label
            block.meta["store_id"] = i + 1  # optional if store_id should follow display order

            # Reposition depending on layout
            if layout == "vertical":
                frame.grid_configure(row=i, column=0)
            else:
                frame.grid_configure(row=0, column=i)


    def addLabeledEntry(self, parent, row, label, variable, state="normal", tooltip=None, validation=None, column=0, vertical=False, columnspan=1):
        """
        Add a labeled entry input field. Supports vertical and horizontal layouts,
        optional tooltips and validation.
        """        
        if vertical:
            tb.Label(parent, text=label).grid(row=row, column=column, columnspan=columnspan, padx=5, pady=(5, 5))
            entry = tb.Entry(parent, textvariable=variable, state=state, width=self.widthEntry)
            entry.grid(row=row + 1, column=column, padx=5, columnspan=columnspan, pady=(0, 10), sticky="ew")
        else:
            tb.Label(parent, text=label).grid(row=row, column=column, padx=5, pady=5, sticky="e")
            entry = tb.Entry(parent, textvariable=variable, state=state, width=self.widthEntry)
            entry.grid(row=row, column=column + 1, columnspan=columnspan, padx=5, pady=5, sticky="ew")

        if tooltip:
            self.addTooltip(entry, tooltip)

        validationFunc = self.resolveValidator(validation) if validation else None
        if callable(validationFunc):
            def onFocusOut(event):
                value = entry.get()
                if validationFunc(value):
                    self.clearInvalid(entry)
                else:
                    self.markInvalid(entry)
            entry.bind("<FocusOut>", onFocusOut)

        return entry

    def addLabeledCombobox(self, parent, row, label, variable, values, tooltip=None, state="readonly", column=0, vertical=False, columnspan=1):
        """Add a labeled combobox dropdown field with options."""
        if vertical:
            tb.Label(parent, text=label).grid(row=row, column=column, columnspan=columnspan, padx=5, pady=(5, 0))
            combo = tb.Combobox(parent, textvariable=variable, values=values, state=state, width=self.widthCombo)
            combo.grid(row=row + 1, column=column, columnspan=columnspan, padx=5, pady=(0, 10))
        else:
            tb.Label(parent, text=label).grid(row=row, column=column, padx=5, pady=5, sticky="e")
            combo = tb.Combobox(parent, textvariable=variable, values=values, state=state, width=self.widthCombo)
            combo.grid(row=row, column=column + 1, columnspan=columnspan, padx=5, pady=5, sticky="ew")

        if tooltip:
            self.addTooltip(combo, tooltip)

        return combo

    def getNextAvailableRow(self, frame: tk.Widget) -> int:
        """
        Return the next available row in a container by checking occupied grid rows.
        """        
        used_rows = [
            child.grid_info().get("row")
            for child in frame.winfo_children()
            if "row" in child.grid_info()
        ]
        return max(used_rows, default=-1) + 1