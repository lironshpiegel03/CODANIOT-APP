# --- SESSION & LOCKING LOGIC ---
import json
import os
from datetime import datetime, timedelta

SESSION_FILE = "sessions.json"
SESSION_LOG_FILE = "session_log.txt"

SESSION_TIMEOUT_MINUTES = 30  # Userים לא פעילים ינוקו לאחר פרק זמן זה

def load_sessions():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception:
            return {}
    return {}

def save_sessions(sessions):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

def log_session_action(action, username, fleet_id=None):
    with open(SESSION_LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {action} | user: {username}"
        if fleet_id is not None:
            line += f" | client: {fleet_id}"
        f.write(line + "\n")

def update_session(fleet_id, username):
    sessions = load_sessions()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key = str(fleet_id) if fleet_id is not None else f"user_{username}"
    sessions[key] = {"user": username, "timestamp": now}
    save_sessions(sessions)
    log_session_action("UPDATE", username, fleet_id)

def clean_old_sessions():
    sessions = load_sessions()
    now = datetime.now()
    cleaned = False
    for key in list(sessions.keys()):
        try:
            t = datetime.strptime(sessions[key]["timestamp"], "%Y-%m-%d %H:%M:%S")
            if (now - t) > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                del sessions[key]
                cleaned = True
        except:
            del sessions[key]
            cleaned = True
    if cleaned:
        save_sessions(sessions)

def check_session_conflict(fleet_id, username, max_seconds=30):
    clean_old_sessions()  # Clean old sessions before checking
    sessions = load_sessions()
    entry = sessions.get(str(fleet_id))
    if not entry:
        return None
    if entry["user"] == username:
        return None
    try:
        t1 = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        t2 = datetime.now()
        delta = (t2 - t1).total_seconds()
        if delta > max_seconds:
            return None
        return entry["user"]
    except Exception:
        return None

def get_highest_continuous_code(codes):
    codes = sorted(set(codes))
    expected = 100
    for code in codes:
        if code != expected:
            break
        expected += 1
    return expected - 1


import tkinter as tk
from tkinter import ttk


def apply_clean_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background_disabled="#f5f7fa", borderwidth=0)
    style.configure("TNotebook.Tab",
                    background_disabled="#dee2e6",
                    foreground="black",
                    font=('Segoe UI', 11, 'bold'),
                    padding=(20, 10))
    style.map("TNotebook.Tab",
              background_disabled=[("selected", "#cfd8dc")],
              expand=[("selected", [1, 1, 1, 0])])
    style.configure("TButton",
                    font=('Segoe UI', 10),
                    padding=6,
                    relief="flat",
                    background_disabled="#f1f3f5")
    style.map("TButton",
              background_disabled=[('active', '#e9ecef')],
              relief=[('pressed', 'sunken')])
    style.configure("TLabel",
                    background_disabled="#ffffff",
                    font=('Segoe UI', 10))
    style.configure("TEntry",
                    padding=5,
                    font=('Segoe UI', 10))
    style.configure("TCombobox",
                    padding=4,
                    font=('Segoe UI', 10))

from tkinter import messagebox, filedialog, simpledialog
import pandas as pd
from datetime import datetime


import json
import os
from datetime import datetime

LOCK_FILE = "locks.json"

def load_locks():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_locks(locks):
    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(locks, f, ensure_ascii=False, indent=2)

def lock_client(fleet_id, username):
    locks = load_locks()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    locks[str(fleet_id)] = {"user": username, "time": now}
    save_locks(locks)

def unlock_client(fleet_id):
    locks = load_locks()
    if str(fleet_id) in locks:
        del locks[str(fleet_id)]
        save_locks(locks)

def check_client_lock(fleet_id):
    locks = load_locks()
    return locks.get(str(fleet_id), None)



import json
import os
from datetime import datetime

SESSION_FILE = "sessions.json"


def load_sessions():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception:
            return {}
    return {}


def save_sessions(sessions):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

def update_session(fleet_id, username):
    sessions = load_sessions()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sessions[str(fleet_id)] = {"user": username, "timestamp": now}
    save_sessions(sessions)


def check_session_conflict(fleet_id, username, max_seconds=30):
    clean_old_sessions()  # Clean old sessions before checking
    sessions = load_sessions()
    entry = sessions.get(str(fleet_id))
    if not entry:
        return None
    if entry["user"] == username:
        return None
    try:
        t1 = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        t2 = datetime.now()
        delta = (t2 - t1).total_seconds()
        if delta > max_seconds:
            return None
        return entry["user"]
    except Exception:
        return None

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("System Login")
        self.root.geometry("300x150")
        self.root.configure(bg='#f5f7fa')

        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=10)



# =============================================
# Function: login
# Description: Handles user authentication.
#              Verifies username and password,
#              and sets user permissions (view/limited/full).
# =============================================
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            df = pd.read_excel("users.xlsx")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file users.xlsx was not found in the directory")
            return

        match = df[(df['Username'] == username) & (df['Password'].astype(str) == password)]
        if not match.empty:
            role = match.iloc[0]['Role']
            self.root.destroy()
            app_root = tk.Tk()
            apply_clean_style()
            CodeManagerApp(app_root, role, username)
            app_root.mainloop()
        else:
            messagebox.showerror("Error", "Username or Password is incorrect")


class CodeManagerApp:
    
    def build_programming_tab(self):
        
        canvas = tk.Canvas(self.notebook, bg="#f5f7fa", highlightthickness=0)
        scroll_y = tk.Scrollbar(self.notebook, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y", in_=self.notebook)
        canvas.pack(fill="both", expand=True)
        self.programming_tab = tk.Frame(canvas, bg="#f5f7fa")  # תוכן ראשי אחיד
        canvas.create_window((0, 0), window=self.programming_tab, anchor='nw')

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.programming_tab.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.programming_tab.bind_all("<MouseWheel>", _on_mousewheel)

        self.notebook.add(canvas, text="תכנותים")


        tk.Label(self.programming_tab, text="חפש לפי FLEET:", bg="#f5f7fa").grid(row=0, column=0, padx=5, pady=5)
        self.programming_search_entry = tk.Entry(self.programming_tab, bg="white")
        self.programming_search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.programming_name_label = tk.Label(self.programming_tab, text="שם לקוח: ", bg="#f5f7fa")
        self.programming_name_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        tk.Button(self.programming_tab, text="חפש", command=self.search_programming_fleet).grid(row=0, column=2, padx=5, pady=5)

        self.programming_fields = [
            'ח.פ',
            'מספר כרטיס מגנטי  1',
            'מספר כרטיס מגנטי  2',
            'בכרטיס מגנטי יש לתכנת תאים 113-177 הערות',
            'כרטיסי עובד נוספים',
            'כרטיסי עובד נוספים.1'
        ]
        self.programming_entries = {}

        for i, field in enumerate(self.programming_fields):
            tk.Label(self.programming_tab, text=field, anchor="w", bg="#f5f7fa").grid(row=i+1, column=0, padx=5, pady=3, sticky="w")
            entry = tk.Entry(self.programming_tab, width=60, bg="white")
            entry.grid(row=i+1, column=1, padx=5, pady=3)
            tk.Button(self.programming_tab, text="📋", command=lambda f=field: self.copy_programming_field(f)).grid(row=i+1, column=2, padx=2)
            self.programming_entries[field] = entry
            entry.config(state='disabled')

                
        if self.role == 'full':
            self.programming_edit_button = tk.Button(self.programming_tab, text="ערוך", command=self.enable_programming_edit)
            self.programming_edit_button.grid(row=len(self.programming_fields)+1, column=0, columnspan=2, pady=10)
        self.programming_save_button = tk.Button(self.programming_tab, text="שמור שינויים", command=self.save_programming_changes)
        self.programming_save_button.grid(row=len(self.programming_fields)+2, column=0, columnspan=2, pady=10)
        self.programming_save_button.config(state='disabled')

    def search_programming_fleet(self):
        fleet = self.programming_search_entry.get().strip()
        if not fleet.isdigit():
            messagebox.showerror("שגיאה", "מספר FLEET לא חוקי")
            return
        fleet = int(fleet)

        matches = self.df[self.df['fleet'] == fleet]
        if matches.empty:
            messagebox.showinfo("לא נמצא", f"לא נמצא לקוח עם FLEET {fleet}")
            return

        if len(matches) > 1:
            matches = matches.reset_index(drop=False)
            options = []
            for i, row in matches.iterrows():
                name = row.get("Name", f"אין שם ({i})")
                options.append(f"{i} - {name}")
            msg = "יש מספר לקוחות עם אותו FLEET.\nבחרי לפי אינדקס:\n" + "\n".join(options)
            choice = simpledialog.askstring("בחר לקוח", msg)
            if choice is None or not choice.strip().isdigit():
                messagebox.showerror("שגיאה", "בחירה לא חוקית")
                return
            index_choice = int(choice.strip())
            if index_choice < 0 or index_choice >= len(matches):
                messagebox.showerror("שגיאה", "בחירה לא חוקית")
                return
            selected_index = matches.loc[index_choice, "index"]
        else:
            selected_index = matches.index[0]

        self.programming_row_index = selected_index
        self.programming_client_name = self.df.at[selected_index, 'Name']
        self.programming_name_label.config(text=f"שׁם לקוח: {self.programming_client_name}")

        for field in self.programming_fields:
            value = self.df.at[self.programming_row_index, field] if field in self.df.columns else ""
            if pd.isna(value):
                value = ""
            self.programming_entries[field].config(state='normal')
            self.programming_entries[field].delete(0, tk.END)
            self.programming_entries[field].insert(0, str(value))
            if self.role != 'edit':
                self.programming_entries[field].config(state='disabled')

        if self.role == 'full':
            self.programming_save_button.config(state='normal')
        else:
            self.programming_save_button.config(state='disabled')
        fleet = self.programming_search_entry.get().strip()
        if not fleet.isdigit():
            messagebox.showerror("שגיאה", "מספר FLEET לא חוקי")
            return
        fleet = int(fleet)

        matches = self.df[self.df['fleet'] == fleet]
        if matches.empty:
            messagebox.showinfo("לא נמצא", f"לא נמצא לקוח עם FLEET {fleet}")
            return

        if len(matches) > 1:
            options = []
            for i, row in matches.iterrows():
                name = row.get("Name", f"אין שם ({i})")
                options.append(f"{i} - {name}")
            msg = "יש מספר לקוחות עם אותו FLEET.\nבחרי לפי אינדקס:\n" + "\n".join(options)
            choice = simpledialog.askstring("בחר לקוח", msg)
            if choice is None or not choice.strip().isdigit() or int(choice) >= len(matches):
                messagebox.showerror("שגיאה", "בחירה לא חוקית")
                return
            selected_index = matches.index[int(choice)]
        else:
            selected_index = matches.index[0]

        self.programming_row_index = selected_index
        self.programming_client_name = self.df.at[selected_index, 'Name']
        self.programming_name_label.config(text=f"שׁם לקוח: {self.programming_client_name}")

        for field in self.programming_fields:
            value = self.df.at[self.programming_row_index, field] if field in self.df.columns else ""
            if pd.isna(value):
                value = ""
            self.programming_entries[field].config(state='normal')
            self.programming_entries[field].delete(0, tk.END)
            self.programming_entries[field].insert(0, str(value))
            if self.role != 'edit':
                self.programming_entries[field].config(state='disabled')

        if self.role == 'full':
            self.programming_save_button.config(state='normal')
        else:
            self.programming_save_button.config(state='disabled')
        fleet = self.programming_search_entry.get().strip()
        if not fleet.isdigit():
            messagebox.showerror("שגיאה", "מספר FLEET לא חוקי")
            return
        fleet = int(fleet)

        matches = self.df[self.df['fleet'] == fleet]
        if matches.empty:
            messagebox.showinfo("לא נמצא", f"לא נמצא לקוח עם FLEET {fleet}")
            return

        if len(matches) > 1:
            options = []
            for i, row in matches.iterrows():
                name = row.get("Name", f"אין שם ({i})")
                options.append(f"{i} - {name}")
            msg = "יש מספר לקוחות עם אותו FLEET.\nבחר לפי אינדקס:\n" + "\n".join(options)
            choice = simpledialog.askstring("בחר לקוח", msg)
            if choice is None or not choice.strip().isdigit() or int(choice) not in matches.index:
                messagebox.showerror("שגיאה", "בחירה לא חוקית")
                return
            selected_index = int(choice)
        else:
            selected_index = matches.index[0]

        self.programming_row_index = selected_index
        self.programming_client_name = self.df.at[selected_index, 'Name']
        self.programming_name_label.config(text=f"שׁם לקוח: {self.programming_client_name}")

        for field in self.programming_fields:
            value = self.df.at[self.programming_row_index, field] if field in self.df.columns else ""
            if pd.isna(value): value = ""
            self.programming_entries[field].config(state='normal')
            self.programming_entries[field].delete(0, tk.END)
            self.programming_entries[field].insert(0, str(value))
            if self.role != 'edit':
                self.programming_entries[field].config(state='disabled')

        if self.role == 'full':
            self.programming_save_button.config(state='normal')
        else:
            self.programming_save_button.config(state='disabled')
        fleet = self.programming_search_entry.get().strip()
        if not fleet.isdigit():
            messagebox.showerror("שגיאה", "מספר FLEET לא חוקי")
            return
        fleet = int(fleet)

        matches = self.df[self.df['fleet'] == fleet]
        if matches.empty:
            messagebox.showinfo("לא נמצא", f"לא נמצא לקוח עם FLEET {fleet}")
            return

        self.programming_row_index = matches.index[0]

        for field in self.programming_fields:
            value = self.df.at[self.programming_row_index, field] if field in self.df.columns else ""
            if pd.isna(value): value = ""
            self.programming_entries[field].config(state='normal')
            self.programming_entries[field].delete(0, tk.END)
            self.programming_entries[field].insert(0, str(value))
            if self.role != 'edit':
                self.programming_entries[field].config(state='disabled')

        if self.role == 'full':
            self.programming_save_button.config(state='normal')
        else:
            self.programming_save_button.config(state='disabled')

    def save_programming_changes(self):
        for field in self.programming_fields:
            self.df.at[self.programming_row_index, field] = self.programming_entries[field].get().strip()
        try:
            self.df.to_excel(self.excel_path, index=False)
            messagebox.showinfo("הצלחה", "הנתונים נשמרו בהצלחה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בשמירה: {e}")

    def __init__(self, root, role, username='מערכת'):
        self.root = root
        self.root.title("Code Management")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.enable_traversal()
        self.notebook.tk.call('ttk::style', 'configure', 'TNotebook.Tab', '-justify', 'right')

        try:
            style = ttk.Style()
            style.theme_use('default')
            style.configure("TNotebook.Tab", padding=[20, 10], font=('Arial', 12, 'bold'))
        except Exception as e:
            print("Style load failed:", e)

        self.notebook.pack(fill="both", expand=True)

        
        canvas_manage = tk.Canvas(self.notebook, bg="#f5f7fa")
        scroll_y_manage = tk.Scrollbar(self.notebook, orient="vertical", command=canvas_manage.yview)
        canvas_manage.configure(yscrollcommand=scroll_y_manage.set)
        scroll_y_manage.pack(side="right", fill="y", in_=self.notebook)
        canvas_manage.pack(fill="both", expand=True)
        self.tab_manage = tk.Frame(canvas_manage, bg="#f5f7fa")
        canvas_manage.create_window((0, 0), window=self.tab_manage, anchor="nw")

        def _on_mousewheel_manage(event):
            canvas_manage.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.tab_manage.bind("<Configure>", lambda e: canvas_manage.configure(scrollregion=canvas_manage.bbox("all")))
        self.tab_manage.bind_all("<MouseWheel>", _on_mousewheel_manage)

        self.window = root
        self.notebook.add(canvas_manage, text="ניהול קודים")


        self.tab_add_client = tk.Frame(self.notebook, bg="#f5f7fa")
        self.notebook.add(self.tab_add_client, text="הוסף לקוח חדש")
        self.window.geometry("1200x800")

        self.role = role
        self.username = username
        self.client_id = None
        self.client_row_index = None
        self.client_name = None
        self.password = "2003"
        self.codes_per_page = 100
        self.current_page = 0
        self.history_data_per_client = {}
        self.last_history_time = None
        self.root.after(1000, self.auto_refresh_history)
        self.root.after(2000, self.update_presence_heartbeat)
        self.build_programming_tab()
        self.client_selection_done = False



        try:
            self.excel_path = "מעקב קודניות.xlsx"
            self.df = pd.read_excel(self.excel_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "הקובץ מעקב קודניות.xlsx לא נמצא בתיקייה")
            root.destroy()
            return

        self.load_history_from_excel()
        self.build_gui()

    def build_gui(self):
        self.build_add_client_tab()
        tk.Label(self.tab_manage, text="FLEET:").grid(row=0, column=0)
        self.client_entry = tk.Entry(self.tab_manage)
        self.client_entry.grid(row=0, column=1)
        tk.Button(self.tab_manage, text="Display Client", command=self.display_client).grid(row=0, column=2)

        tk.Label(self.tab_manage, text="Order Number:").grid(row=0, column=3)
        self.order_entry = tk.Entry(self.tab_manage)
        self.order_entry.grid(row=0, column=4)

        tk.Button(self.tab_manage, text="Refresh", command=self.display_client).grid(row=0, column=5)
        tk.Button(self.tab_manage, text="Release Lock", command=self.release_lock).grid(row=0, column=6)
        tk.Button(self.tab_manage, text="Logout from Client", command=self.logout_from_client).grid(row=0, column=7)

        self.info_label = tk.Label(self.tab_manage, text="")
        self.info_label.grid(row=1, column=0, columnspan=6)

        self.codes_frame = tk.Frame(self.tab_manage)
        self.codes_frame.grid(row=2, column=0, columnspan=6)

        self.nav_label = tk.Label(self.tab_manage, text="")
        self.nav_label.grid(row=6, column=2, columnspan=2)

        self.history_frame = tk.Frame(self.tab_manage)
        self.history_frame.grid(row=7, column=0, columnspan=6)

        tk.Label(self.tab_manage, text="Reserve Range:").grid(row=3, column=0)
        self.range_entry = tk.Entry(self.tab_manage)
        self.range_entry.grid(row=3, column=1)
        self.reserve_button = tk.Button(self.tab_manage, text="Reserve", command=self.reserve_range)
        self.reserve_button.grid(row=3, column=2)

        tk.Label(self.tab_manage, text="Reserve Amount:").grid(row=4, column=0)
        self.amount_entry = tk.Entry(self.tab_manage)
        self.amount_entry.grid(row=4, column=1)
        self.amount_button = tk.Button(self.tab_manage, text="Reserve לפי כמות", command=self.reserve_by_amount)
        self.amount_button.grid(row=4, column=2)

        tk.Label(self.tab_manage, text="Release Code:").grid(row=5, column=0)
        self.release_entry = tk.Entry(self.tab_manage)
        self.release_entry.grid(row=5, column=1)
        tk.Label(self.tab_manage, text="Password:").grid(row=5, column=2)
        self.password_entry = tk.Entry(self.tab_manage)
        self.password_entry.grid(row=5, column=3)
        self.release_button = tk.Button(self.tab_manage, text="Release Code", command=self.release_codes)
        self.release_button.grid(row=5, column=4)

        tk.Button(self.tab_manage, text="<< Previous", command=self.prev_page).grid(row=6, column=0)
        tk.Button(self.tab_manage, text="Next >>", command=self.next_page).grid(row=6, column=1)
        self.nav_label = tk.Label(self.tab_manage, text="")
        self.nav_label.grid(row=6, column=2, columnspan=2)

        self.history_frame = tk.Frame(self.tab_manage)
        self.history_frame.grid(row=7, column=0, columnspan=6)

        self.export_button = tk.Button(self.tab_manage, text="Export History to Excel", command=self.export_history)
        self.export_button.grid(row=8, column=0, columnspan=2)
        tk.Label(self.tab_manage, text="Filter History").grid(row=9, column=0, columnspan=2, pady=10)

        tk.Label(self.tab_manage, text="Username:").grid(row=10, column=0)
        tk.Label(self.tab_manage, text="Client Name:").grid(row=10, column=4)
        client_names = sorted(self.df['Name'].dropna().astype(str).unique().tolist())
        self.search_clientname_entry = ttk.Combobox(self.tab_manage, values=client_names)
        self.search_clientname_entry.grid(row=10, column=5)
        self.search_clientname_entry.bind("<<ComboboxSelected>>", lambda e: self.filter_history())
        self.search_clientname_entry.grid(row=10, column=5)
        self.search_name_entry = tk.Entry(self.tab_manage)
        self.search_name_entry.grid(row=10, column=1)

        tk.Label(self.tab_manage, text="FLEET:").grid(row=10, column=2)
        self.search_id_entry = tk.Entry(self.tab_manage)
        self.search_id_entry.grid(row=10, column=3)

        tk.Label(self.tab_manage, text="From Date (YYYY-MM-DD):").grid(row=11, column=0)
        self.date_from_entry = tk.Entry(self.tab_manage)
        self.date_from_entry.grid(row=11, column=1)

        tk.Label(self.tab_manage, text="To Date:").grid(row=11, column=2)
        self.date_to_entry = tk.Entry(self.tab_manage)
        self.date_to_entry.grid(row=11, column=3)

        tk.Button(self.tab_manage, text="Search", command=self.filter_history).grid(row=11, column=4)


        if self.role == 'view':
            self.reserve_button.config(state='disabled')
            self.amount_button.config(state='disabled')
            self.release_button.config(state='disabled')
        # הרשאת limited מאפשרת גם שחרור קודים – לכן לא נבצע חסימה


    def display_client(self):
        self.client_selection_done = False  # תוקן - תמיד לבחור מחדש
        if self.df is None:
            messagebox.showerror("Error", "הקובץ לא נטען")
            return
        try:
            client_id = int(self.client_entry.get())
        except ValueError:
            messagebox.showerror("Error", "FLEET לא תקין")
            return


        # בדיקת נעילה
        lock = check_client_lock(client_id)
        if lock and lock["user"] != self.username:
            messagebox.showwarning("Warning", f"Attention: the user {lock['user']} is also working on this client")
        else:
            lock_client(client_id, self.username)


        # ניהול נוכחות חיה
        conflict_user = check_session_conflict(client_id, self.username)
        if conflict_user:
            messagebox.showwarning("Conflict", f"The user {conflict_user} is already editing this client")
        update_session(client_id, self.username)

        match = self.df[self.df['fleet'] == client_id]
        if match.empty:
            messagebox.showerror("Error", "Client not found")
            return

        if not self.client_selection_done:
            if len(match) > 1:
                options = []
                for i, row in match.iterrows():
                    name = row.get("Name", f"אין שם ({i})")
                    options.append(f"{i} - {name}")
                msg = "יש FLEETות עם אותו מספר FLEET.\nSelect by index:\n" + "\n".join(options)
                choice = simpledialog.askstring("Select Client", msg)
                if choice is None or not choice.strip().isdigit() or int(choice) not in match.index:
                    messagebox.showerror("Error", "Invalid selection")
                    return
                self.client_row_index = int(choice)
            else:
                self.client_row_index = match.index[0]
            self.client_selection_done = True
        selected_index = self.client_row_index

        self.client_id = client_id
        self.client_row_index = selected_index
        self.client_name = self.df.at[selected_index, 'Name']
        self.info_label.config(text=f"FLEET: {self.client_id} | שם: {self.client_name}")

        for widget in self.codes_frame.winfo_children():
            widget.destroy()

        taken = set(self.get_taken_codes())
        page_start = 100 + self.current_page * self.codes_per_page
        page_codes = list(range(page_start, page_start + self.codes_per_page))
        for i, code in enumerate(page_codes):
            color = "red" if code in taken else "green"
            tk.Label(self.codes_frame, text=str(code), bg=color, width=4).grid(row=i//10, column=i%10)

        self.nav_label.config(text=f"קוד אחרון פנוי הבא: {self.get_next_free_code(taken)}")
        self.update_history_table()

    
    def get_taken_codes(self):
        row = self.df.loc[self.client_row_index]
        taken_raw = row.get('taken list')

        # If taken list is empty but driver id exists, generate auto taken list
        if (pd.isna(taken_raw) or str(taken_raw).strip() == "") and not pd.isna(row.get("driver id")):
            try:
                driver_id = int(row.get("driver id"))
                if driver_id >= 100:
                    auto_taken = f"100-{driver_id}"
                    self.df.at[self.client_row_index, 'taken list'] = str(auto_taken)
                    taken_raw = auto_taken
            except:
                pass

        if pd.isna(taken_raw):
            return []

        taken_ranges = str(taken_raw).split(",")
        codes = set()
        for rng in taken_ranges:
            rng = rng.strip()
            if "-" in rng:
                try:
                    start, end = map(int, rng.split("-"))
                    codes.update(range(start, end + 1))
                except:
                    continue
            elif rng.isdigit():
                codes.add(int(rng))
        return codes


    def get_next_free_code(self, taken, max_code=1000000):
        for code in range(100, max_code):
            if code not in taken:
                return code
        return "אין"

    def parse_range(self, rng):
        result = []
        parts = rng.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                result.extend(range(start, end+1))
            elif part.strip().isdigit():
                result.append(int(part))
        return result

    def compress_ranges(self, codes):
        if not codes:
            return []
        codes.sort()
        ranges = []
        start = prev = codes[0]
        for c in codes[1:]:
            if c == prev + 1:
                prev = c
            else:
                ranges.append(f"{start}-{prev}" if start != prev else str(start))
                start = prev = c
        ranges.append(f"{start}-{prev}" if start != prev else str(start))
        return ranges



# =============================================
# Function: reserve_range
# Description: Reserves a specific range of codes
#              for a selected client. Checks for
#              overlapping or already reserved codes.
# =============================================
    def reserve_range(self):
        order_number = self.order_entry.get().strip()
        if not order_number:
            messagebox.showerror("Error", "נא להזין Order Number")
            return

        if not messagebox.askyesno("אישור", "Are you sure?"):
            return

        rng = self.range_entry.get()
        new_codes = self.parse_range(rng)
        taken = set(self.get_taken_codes())
        if any(code in taken for code in new_codes):
            messagebox.showerror("Error", "חלק מהקודים כבר Reserveים")
            return

        idx = self.client_row_index
        combined = sorted(set(taken.union(new_codes)))
        main_code = get_highest_continuous_code(combined)
        self.df.at[idx, 'driver id'] = main_code

        # שמירה לעמודת taken list לצורך צביעה
        full_range = self.compress_ranges(combined)
        self.df.at[idx, 'taken list'] = ",".join(full_range)

        leftover = sorted(set(combined) - set(range(100, main_code + 1)))
        existing_comment = str(self.df.at[idx, 'הערה']) if not pd.isna(self.df.at[idx, 'הערה']) else ""
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"
        existing_comment = str(self.df.at[idx, 'הערה']) if not pd.isna(self.df.at[idx, 'הערה']) else ""
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"
        existing_comment = str(self.df.at[idx, 'הערה']) if not pd.isna(self.df.at[idx, 'הערה']) else ""
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"

        self.df.to_excel(self.excel_path, index=False)

        self.log_action("Reserve", rng)
        self.update_history_table()


    def reserve_by_amount(self):
        order_number = self.order_entry.get().strip()
        if not order_number:
            messagebox.showerror("Error", "נא להזין Order Number")
            return

        amount = self.amount_entry.get().strip()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid number")
            return

        amount = int(amount)
        taken = set(self.get_taken_codes())
        new_codes = []
        next_code = self.get_next_free_code(taken)
        if next_code == "אין":
            messagebox.showerror("Error", "No available codes")
            return

        for _ in range(amount):
            while next_code in taken:
                next_code += 1
                if next_code > 1000000:
                    messagebox.showerror("Error", "Not enough available codes")
                    return
            new_codes.append(next_code)
            taken.add(next_code)

        # Temporary visual update before confirmation
        self.temp_reserved_codes = new_codes
        self.update_temp_visual()
        messagebox.showinfo("Success", f"Codes taken: {', '.join(map(str, new_codes))}")
        if messagebox.askokcancel("אישור", f"Codes taken: {', '.join(map(str, new_codes))}"):
            self.reserve_range_of_codes(new_codes)




# =============================================
# Function: reserve_range
# Description: Reserves a specific range of codes
#              for a selected client. Checks for
#              overlapping or already reserved codes.
# =============================================
    def reserve_range_of_codes(self, codes):
        idx = self.client_row_index
        taken = set(self.get_taken_codes())
        combined = sorted(set(taken.union(codes)))
        main_code = get_highest_continuous_code(combined)
        self.df.at[idx, 'driver id'] = main_code

        full_range = self.compress_ranges(combined)
        self.df.at[idx, 'taken list'] = ",".join(full_range)

        leftover = sorted(set(combined) - set(range(100, main_code + 1)))
        existing_comment = str(self.df.at[idx, 'הערה']) if not pd.isna(self.df.at[idx, 'הערה']) else ""
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"
        if leftover:
            leftover_str = ','.join(map(str, leftover))
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Taken {leftover_str} - {pd.Timestamp.today().date()}"
        else:
            if not existing_comment.strip():
                self.df.at[idx, 'הערה'] = f"Continuous until {main_code} - {pd.Timestamp.today().date()}"

        self.df.to_excel(self.excel_path, index=False)
        self.log_action("Reserve", ','.join(map(str, codes)))
        self.display_client()


    def release_codes(self):
        order_number = self.order_entry.get().strip()
        if not order_number:
            messagebox.showerror("Error", "Please enter order number")
            return

        rng = self.release_entry.get()
        pwd = self.password_entry.get()
        if pwd != self.password:
            messagebox.showerror("Wrong Password", "Access denied to release codes")
            return

        release_set = set(self.parse_range(rng))
        idx = self.client_row_index
        original = str(self.df.at[idx, 'taken list']).split(",") if not pd.isna(self.df.at[idx, 'taken list']) else []
        current_codes = []
        for segment in original:
            current_codes.extend(self.parse_range(segment))

        updated_codes = sorted(set(current_codes) - release_set)

        # Update driver id
        main_code = get_highest_continuous_code(updated_codes)
        self.df.at[idx, 'driver id'] = main_code if updated_codes else None

        # Update taken list
        new_ranges = self.compress_ranges(updated_codes)
        self.df.at[idx, 'taken list'] = ",".join(new_ranges) if new_ranges else None

        # Update comment
        self.df.at[idx, 'הערה'] = f"שוחרר {rng} - {pd.Timestamp.today().date()}"

        self.df.to_excel(self.excel_path, index=False)
        self.log_action("Release", rng)
        self.display_client()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_client()

    def next_page(self):
        self.current_page += 1
        self.display_client()

    def export_history(self):
        key = f"{self.client_id}_{self.client_row_index}"
        if key not in self.history_data_per_client:
            messagebox.showerror("Error", "No history found for this client")
            return
        entries = self.history_data_per_client[key]
        rows = []
        for entry in entries:
            parts = entry.split(" | ")
            date = parts[0]
            client = parts[0].split("לקוח ")[1]
            action = parts[1].split(": ")[1]
            code_range = parts[2].split(": ")[1]
            order_num = parts[3].split(": ")[1]
            rows.append({
                "Date": date,
                "User": parts[4].split(": ")[1] if len(parts) > 4 else "לא ידוע",
                "Action": action,
                "Code/Range": code_range,
                "Order Number": order_num,
                "FLEET": client
            })
        df = pd.DataFrame(rows)
        file_path = f"History_Client_{self.client_id}.xlsx"
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"The file has been saved as {file_path}")



    def load_history_from_excel(self):
        try:
            self.history_df = pd.read_excel("history.xlsx")
        except FileNotFoundError:
            self.history_df = pd.DataFrame(columns=["Date", "User", "Action", "Code/Range", "Order Number", "FLEET"])

    def save_history_to_excel(self):
        self.history_df.to_excel("history.xlsx", index=False)

    def log_action(self, action_type, code_range):
        if self.client_id is not None:
            order_number = self.order_entry.get().strip() or "ללא"
            new_entry = {
                "Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "User": self.username,
                "Action": action_type,
                "Code/Range": code_range,
                "Order Number": order_number,
                "FLEET": self.client_id
            }
            new_entry_df = pd.DataFrame([new_entry])
            self.history_df = pd.concat([self.history_df, new_entry_df], ignore_index=True)
            self.save_history_to_excel()
            self.update_history_table()





# =============================================
# Function: filter_history
# Description: Filters the displayed history records
#              by client ID, date range, or order.
# =============================================
    def filter_history(self):
        client_name = self.search_clientname_entry.get().strip()
        name = self.search_name_entry.get().strip()
        client_id = self.search_id_entry.get().strip()
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()

        df = self.history_df.copy()

        if name:
            df = df[df["User"].str.contains(name, na=False)]

        if client_id:
            df = df[df["FLEET"].astype(str) == client_id]

        if date_from:
            df = df[df["Date"] >= date_from]
        if date_to:
            df = df[df["Date"] <= date_to]

        if client_name:
            name_matches = self.df[self.df['Name'].astype(str).str.contains(client_name, case=False, na=False)]
            fleets = name_matches['fleet'].astype(str).tolist()
            df = df[df['FLEET'].astype(str).isin(fleets)]
        self.display_filtered_history(df)

    def display_filtered_history(self, df):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        tk.Label(self.history_frame, text="תוצאות Filter History", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=6)
        headers = ["Date", "Action", "Code/Range", "Order Number", "FLEET", "User"]
        for i, header in enumerate(headers):
            tk.Label(self.history_frame, text=header, relief="solid", width=20).grid(row=1, column=i)

        for r, entry in df.iterrows():
            values = [entry[col] for col in headers]
            for c, v in enumerate(values):
                tk.Label(self.history_frame, text=v, relief="ridge", width=20).grid(row=r+2, column=c)





# =============================================
# Function: update_history
# Description: Records all actions (reserve/release)
#              into the client history Excel sheet.
# =============================================
    def update_history_table(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        tk.Label(self.history_frame, text="Recent History Log", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=6)

        headers = ["Date", "Action", "Code/Range", "Order Number", "FLEET", "User"]
        for i, header in enumerate(headers):
            tk.Label(self.history_frame, text=header, relief="solid", width=20).grid(row=1, column=i)

        # Try to find client history using either English or Hebrew column name
        if "FLEET" in self.history_df.columns:
            client_history_df = self.history_df[self.history_df["FLEET"].astype(str) == str(self.client_id)]
        elif "מספר לקוח" in self.history_df.columns:
            client_history_df = self.history_df[self.history_df["מספר לקוח"].astype(str) == str(self.client_id)]
        else:
            client_history_df = pd.DataFrame()  # Empty DataFrame if neither column found

        # Last 6 entries
        last_entries = client_history_df.tail(6)

        for r, entry in enumerate(last_entries.itertuples(index=False), start=2):
            values = [entry[0], entry[2], entry[3], entry[4], entry[5], entry[1]]
            for c, val in enumerate(values):
                tk.Label(self.history_frame, text=str(val), relief="ridge", width=20).grid(row=r, column=c)

    def release_lock(self):
        if self.client_id is not None:
            unlock_client(self.client_id)
            messagebox.showinfo("שחרור", "הנעילה Releasedה. ניתן לטעון מחדש את הלקוח.")



    def auto_refresh_history(self):
        try:
            path = "history.xlsx"
            if os.path.exists(path):
                current_time = os.path.getmtime(path)
                if self.last_history_time is None or current_time > self.last_history_time:
                    self.last_history_time = current_time
                    self.load_history_from_excel()
                    self.df = pd.read_excel(self.excel_path)  # טען מחדש את הקובץ עם הקודים
                    self.display_client()  # עדכן תצוגה כולל צבעים
        except Exception as e:
            print("Error בעדכון אוטומטי:", e)
        self.tab_manage.after(1000, self.auto_refresh_history)
        self.tab_manage.after(2000, self.update_presence_heartbeat)





    def build_add_client_tab(self):
        fields = [
            'Name', 'fleet', 'driver id', 'הערה', 'ח.פ',
            'מספר כרטיס מגנטי  1', 'מספר כרטיס מגנטי  2',
            'בכרטיס מגנטי יש לתכנת תאים 113-177 הערות',
            'כרטיסי עובד נוספים', 'כרטיסי עובד נוספים.1',
            'taken list'
        ]
        self.add_client_entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(self.tab_add_client, text=field, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=3, sticky="w")
            entry = tk.Entry(self.tab_add_client, width=40)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.add_client_entries[field] = entry

        self.allow_duplicate_var = tk.BooleanVar(value=False)
        duplicate_checkbox = tk.Checkbutton(
            self.tab_add_client,
            text="מדובר באותו לקוח (אפשר כפילות FLEET)",
            variable=self.allow_duplicate_var
        )
        duplicate_checkbox.grid(row=len(fields), column=0, columnspan=2, pady=5)

        save_button = tk.Button(self.tab_add_client, text="שמור לקוח חדש", command=self.save_new_client)
        save_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        if self.role != 'full':
            save_button.config(state='disabled')

        delete_button = tk.Button(self.tab_add_client, text="הסר לקוח", command=self.delete_client)
        delete_button.grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
        if self.role != 'full':
            delete_button.config(state='disabled')

    
    def save_new_client(self):
        data = {field: self.add_client_entries[field].get().strip() for field in self.add_client_entries}
        if not data["Name"] or not data["fleet"]:
            messagebox.showerror("שגיאה", "נא למלא שם לקוח ו-FLEET")
            return
        try:
            data["fleet"] = int(data["fleet"])
        except ValueError:
            messagebox.showerror("שגיאה", "FLEET חייב להיות מספר")
            return

        if os.path.exists(self.excel_path):
            df = pd.read_excel(self.excel_path)
        else:
            df = pd.DataFrame(columns=data.keys())

        if not self.allow_duplicate_var.get() and data["fleet"] in df["fleet"].values:
            messagebox.showwarning("שגיאה", "FLEET כבר קיים. סמן את התיבה אם מדובר באותו לקוח")
            return

        df.loc[len(df)] = data
        df.to_excel(self.excel_path, index=False)

        # רענון הנתונים גם בטאב ניהול
        self.df = pd.read_excel(self.excel_path)

        # ניקוי שדות
        for entry in self.add_client_entries.values():
            entry.delete(0, tk.END)

        messagebox.showinfo("הצלחה", "לקוח נוסף בהצלחה. ניתן להציג אותו מיד בטאב ניהול.")

        # טען את הלקוח החדש בטאב ניהול
        self.client_entry.delete(0, tk.END)
        self.client_entry.insert(0, str(data["fleet"]))
        self.display_client()

    def logout_from_client(self):
        if self.client_id is not None:
            unlock_client(self.client_id)
            sessions = load_sessions()
            if str(self.client_id) in sessions and sessions[str(self.client_id)]["user"] == self.username:
                del sessions[str(self.client_id)]
                save_sessions(sessions)
                log_session_action("LOGOUT", self.username, self.client_id)
            messagebox.showinfo("Logout", "You have been logged out from the client.")
            self.client_id = None
            self.client_row_index = None
            self.client_name = None
            self.client_entry.delete(0, tk.END)
            self.info_label.config(text="")
            for widget in self.codes_frame.winfo_children():
                widget.destroy()



    
    def delete_client(self):
        fleet = self.add_client_entries["fleet"].get().strip()
        if not fleet:
            messagebox.showerror("שגיאה", "נא להזין FLEET")
            return
        try:
            fleet = int(fleet)
        except ValueError:
            messagebox.showerror("שגיאה", "FLEET חייב להיות מספר")
            return

        if not messagebox.askyesno("אישור", f"האם את בטוחה שברצונך למחוק את הלקוח עם FLEET {fleet}?"):
            return

        df = pd.read_excel(self.excel_path)
        new_df = df[df["fleet"] != fleet]
        if len(new_df) == len(df):
            messagebox.showinfo("מידע", "לא נמצא לקוח למחיקה")
        else:
            new_df.to_excel(self.excel_path, index=False)
            messagebox.showinfo("הצלחה", f"הלקוח עם FLEET {fleet} נמחק")
            for entry in self.add_client_entries.values():
                entry.delete(0, tk.END)
            self.df = new_df


    def update_presence_heartbeat(self):
        if self.client_id:
            update_session(self.client_id, self.username)
        self.tab_manage.after(2000, self.update_presence_heartbeat)


    def copy_programming_field(self, field):
        value = self.programming_entries[field].get().strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        messagebox.showinfo("הועתק", f"הטקסט \"{value}\" הועתק לזיכרון")



    def enable_programming_edit(self):
        if self.role != "full": return
        for field in self.programming_fields:
            self.programming_entries[field].config(state='normal')
        self.programming_save_button.config(state='normal')


    def update_temp_visual(self):
        # Temporary orange highlight
        for widget in self.codes_frame.winfo_children():
            widget.destroy()
        taken = set(self.get_taken_codes())
        temp = set(getattr(self, "temp_reserved_codes", []))
        page_start = 100 + self.current_page * self.codes_per_page
        page_codes = list(range(page_start, page_start + self.codes_per_page))
        for i, code in enumerate(page_codes):
            if code in temp:
                color = "orange"
            elif code in taken:
                color = "red"
            else:
                color = "green"
            tk.Label(self.codes_frame, text=str(code), bg=color, width=4).grid(row=i//10, column=i%10)


    def update_temp_visual(self):
        # Temporary orange highlight
        for widget in self.codes_frame.winfo_children():
            widget.destroy()
        taken = set(self.get_taken_codes())
        temp = set(getattr(self, "temp_reserved_codes", []))
        page_start = 100 + self.current_page * self.codes_per_page
        page_codes = list(range(page_start, page_start + self.codes_per_page))
        for i, code in enumerate(page_codes):
            if code in temp:
                color = "orange"
            elif code in taken:
                color = "red"
            else:
                color = "green"
            tk.Label(self.codes_frame, text=str(code), bg=color, width=4).grid(row=i//10, column=i%10)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        LoginWindow(root)
        root.mainloop()
    except Exception as e:
        import traceback
        messagebox.showerror("Error", f"Error: {e}\n{traceback.format_exc()}")
