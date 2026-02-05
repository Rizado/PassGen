import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import string
import locale
import gettext
import os

locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

LANG_MAP = {
    'russian': 'ru',
    'ru': 'ru',
    'spanish': 'es',
    'es': 'es',
}

lang_code = 'en'

try:
    locale.setlocale(locale.LC_ALL, '')
    sys_locale_tuple = locale.getlocale()
    sys_lang_str = sys_locale_tuple[0]

    if sys_lang_str:
        detected_key = sys_lang_str.partition('_')[0].lower()
        lang_code = LANG_MAP.get(detected_key, 'en')

except Exception as e:
    print(f"Locale error: {e}")
    lang_code = 'en'

mo_filename = os.path.join(locales_dir, f"{lang_code}.mo")

try:
    with open(mo_filename, "rb") as fp:
        trans = gettext.GNUTranslations(fp)
        _ = trans.gettext
except (IOError, OSError, FileNotFoundError):
    _ = lambda s: s


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root

        self.root.title(_("Password Generator"))
        self.root.geometry("650x450")
        self.root.minsize(640, 400)

        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor="n")
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        lbl_length = tk.Label(left_frame, text=_("Password Length (8-24):"))
        lbl_length.pack(pady=(5, 0), anchor="w")
        self.length_var = tk.IntVar(value=12)
        tk.Scale(left_frame, from_=8, to=24, orient=tk.HORIZONTAL, variable=self.length_var, length=250).pack(anchor="w")

        lbl_count = tk.Label(left_frame, text=_("Quantity (1-20):"))
        lbl_count.pack(pady=(5, 0), anchor="w")
        self.count_var = tk.IntVar(value=4)
        tk.Scale(left_frame, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.count_var, length=250).pack(anchor="w")

        self.chk_frame = tk.Frame(left_frame)
        self.chk_frame.pack(pady=10, anchor="w", fill=tk.X)

        self.var_lower = tk.BooleanVar(value=True)
        tk.Checkbutton(self.chk_frame, text=_("Lowercase (a-z) [Required]"), variable=self.var_lower, state="disabled").pack(anchor="w")

        self.var_upper = tk.BooleanVar(value=True)
        tk.Checkbutton(self.chk_frame, text=_("Uppercase (A-Z)"), variable=self.var_upper).pack(anchor="w")

        self.var_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(self.chk_frame, text=_("Digits (0-9)"), variable=self.var_digits).pack(anchor="w")

        self.var_special = tk.BooleanVar(value=False)
        self.spec_chars = "!@#$%^&*()_-=+.,?:;"
        spec_text = f"{_('Special chars')} ({self.spec_chars})"
        tk.Checkbutton(self.chk_frame, text=spec_text, variable=self.var_special).pack(anchor="w")

        self.var_exclude_similar = tk.BooleanVar(value=True)
        tk.Checkbutton(self.chk_frame, text=_("Exclude similar (O/0, I/l/1)"), variable=self.var_exclude_similar).pack(anchor="w", pady=(10, 0))

        btn_generate = tk.Button(left_frame, text=_("Generate"), command=self.generate_passwords, height=2, bg="#e1e1e1")
        btn_generate.pack(fill=tk.X, pady=(20, 0))

        lbl_res = tk.Label(right_frame, text=_("Generated Passwords:"), font=("Arial", 10, "bold"))
        lbl_res.pack(anchor="w", pady=(0, 5))

        self.txt_output = scrolledtext.ScrolledText(right_frame, state='disabled', font=("Consolas", 12))
        self.txt_output.pack(fill=tk.BOTH, expand=True)

    def generate_passwords(self):
        length = self.length_var.get()
        count = self.count_var.get()

        pool_lower = string.ascii_lowercase
        pool_upper = string.ascii_uppercase if self.var_upper.get() else ""
        pool_digits = string.digits if self.var_digits.get() else ""
        pool_special = self.spec_chars if self.var_special.get() else ""

        similar_chars = "Il1O0"

        def filter_chars(chars):
            if self.var_exclude_similar.get():
                return "".join(c for c in chars if c not in similar_chars)
            return chars

        active_pools = []

        if (cl := filter_chars(pool_lower)): active_pools.append(cl)
        if (cu := filter_chars(pool_upper)): active_pools.append(cu)
        if (cd := filter_chars(pool_digits)): active_pools.append(cd)
        if (cs := filter_chars(pool_special)): active_pools.append(cs)

        if not active_pools:
            messagebox.showerror(_("Error"), _("No characters available for generation!"))
            return

        passwords = []
        for _ in range(count):
            current_password = []
            for pool in active_pools:
                current_password.append(random.choice(pool))

            all_chars = "".join(active_pools)
            remaining_len = length - len(current_password)
            if remaining_len > 0:
                current_password.extend(random.choices(all_chars, k=remaining_len))

            random.shuffle(current_password)
            passwords.append("".join(current_password))

        self.txt_output.config(state='normal')
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, "\n".join(passwords))
        self.txt_output.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
