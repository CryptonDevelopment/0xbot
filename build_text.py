import os

import polib


locales_path = "./locales"

for locale_dir in os.listdir(locales_path):
    po_dir = os.path.join(locales_path, locale_dir, "LC_MESSAGES")
    if os.path.isdir(po_dir):
        for po_file in os.listdir(po_dir):
            if po_file.endswith(".po"):
                po_filepath = os.path.join(po_dir, po_file)
                mo_filepath = os.path.join(
                    po_dir, po_file.replace(".po", ".mo")
                )
                po = polib.pofile(po_filepath)
                po.save_as_mofile(mo_filepath)
                print(f"Compiled {po_filepath} to {mo_filepath}")
