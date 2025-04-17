# Jabs Mimir

**Jabs Mimir** is a lightweight, extensible UI micro-framework built on top of `tkinter` and `ttkbootstrap`, designed for rapid internal tool development and structured form workflows.

It provides:

- Reusable UI primitives with validation and tooltips
- Support for block-based form components with dynamic variable binding
- Integration with custom validation logic (via resolver, file loader, or direct function)
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

        # Option 1: Inline validator resolver (string-based)
        self.ui.setValidatorResolver(lambda name: {
            "not_empty": lambda val: bool(str(val).strip())
        }.get(name))

        # Option 2 (alternative): load from file
        # self.ui.setValidatorFile("include/validator.py")

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

Jabs Mimir supports **both automatic and manual validation**, triggered on field focus-out and verified again when clicking "Nästa".

### You can define validation in two ways:

#### 1. **String-based validation (via file or resolver)**

**Define a validator in a file**:
```python
# include/validator.py
def not_empty(value):
    return bool(str(value).strip())
```

**Load it**:
```python
self.ui.setValidatorFile("include/validator.py")
```

**Use string key in field**:
```python
{"label": "Name", "variable": tk.StringVar(), "validation": "not_empty"}
```

#### 2. **Direct function reference**

```python
from include.validator import not_empty

fields = [
    {"label": "Name", "variable": tk.StringVar(), "validation": not_empty}
]
```

✅ Both methods are fully supported and interchangeable.

Mimir automatically:
- Binds validation on focus-out
- Stores all validators internally
- Re-validates all fields when clicking "Nästa"
- Blocks navigation if any invalid inputs remain
- Highlights invalid fields with red styling

Works even for readonly fields (like file upload paths), which normally can't be focused.

---

## Components

### `Mimir`
Manages UI views, tooltips, validation, field rendering, and form logic.
Supports reusable custom field types via `registerFieldType()`.

### `DataBlockWrapper`
A wrapper for block-level form metadata and values. Supports dot-access and `.get()`/`.set()` calls.

### `UtilityModule`
Helper methods for building field metadata, extracting values, validating blocks, and block meta handling.

---

## License
MIT License © 2025 William Lydahl