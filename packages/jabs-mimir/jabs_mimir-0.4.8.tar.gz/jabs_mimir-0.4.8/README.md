# Jabs Mimir

**Jabs Mimir** is a lightweight, extensible UI micro-framework built on top of `tkinter` and `ttkbootstrap`, designed for rapid internal tool development and structured form workflows.

It provides:

- Reusable UI primitives with validation and tooltips
- Support for block-based form components with dynamic variable binding
- Integration with custom validation logic (via resolver or direct functions)
- Modular architecture suitable for internal tooling and small boilerplate projects

---

## Installation

```bash
pip install jabs-mimir
```

---

## Quick Start

```python
from jabs_mimir import Mimir, DataBlockWrapper, UtilityModule
import tkinter as tk
import ttkbootstrap as tb

class App(tb.Window):
    def __init__(self):
        super().__init__(title="Mimir Demo")
        self.ui = Mimir(self)
        self.ui.setValidatorResolver(lambda name: {"not_empty": lambda val: bool(val.strip())}.get(name))

        self.ui.switchView(self.mainView)

    def mainView(self, ui, *args):
        frame = tb.Frame(self)
        fields = [
            {"type": "heading", "label": "Basic Info"},
            {"label": "Name", "key": "name", "variable": tk.StringVar(), "validation": "not_empty"},
            {"label": "Age", "key": "age", "variable": tk.IntVar()}
        ]

        meta = UtilityModule.buildBlockMeta(fields)
        block = DataBlockWrapper(meta)

        ui.renderFields(frame, fields)
        ui.addNextButton(frame, row=len(fields)+1, command=lambda: print(UtilityModule.getBlockValues(block)))

        return frame

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## Validation

You can validate fields in two ways:

### 1. **Using a validator file**

Create a `validator.py`:

```python
# include/validator.py
def not_empty(val):
    return bool(str(val).strip())
```

Load it in your app:

```python
self.ui.setValidatorFile("include/validator.py")
```

And use string keys in fields:

```python
{"label": "Name", "key": "name", "variable": tk.StringVar(), "validation": "not_empty"}
```

### 2. **Using a direct function reference**

Import the function and assign it directly:

```python
from include.validator import not_empty

fields = [
    {"label": "Name", "key": "name", "variable": tk.StringVar(), "validation": not_empty}
]
```

Both styles are supported, and Mimir automatically handles focus-out validation, red border styling, and prevents advancement if any fields are invalid.

---

## Components

### `Mimir`
Manages UI views, tooltips, validation, field rendering, and form logic.

### `DataBlockWrapper`
A wrapper for block-level form metadata and values. Supports dot-access and `.get()`/`.set()` calls.

### `UtilityModule`
Helper methods for building field metadata, extracting values, validating blocks, etc.

---

## License
MIT License © 2025 William Lydahl