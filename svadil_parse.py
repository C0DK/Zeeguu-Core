from svadilparse_python.parse import ModuleInspector
import zeeguu_core

elms = ModuleInspector(zeeguu_core).get_all_items_in_module_and_submodule()
print("\n\n We found the following items")
for elm in elms:
    print(
        "####",
        "Name:",
        " " + elm.name,
        "Type:",
        " " + elm.of_type.name,
        "Descripton:",
        " " + (elm.description or "N/A"),
        sep="\n",
    )
