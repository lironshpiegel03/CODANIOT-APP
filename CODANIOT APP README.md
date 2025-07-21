# 🧠 CODANIOT APP — Code & SIM Management System

A Python-based desktop application for managing  codes, client identifiers (FLEETs), and magnetic programming data. Designed for lab technicians and internal operations teams, this app enables accurate tracking, code locking, role-based permissions, and Excel integration.

---

## ✨ Features

- 🔍 Search and load client data by `FLEET`
- ✅ Visual code reservation with real-time color indicators:
  - Green = available  
  - Red = taken  
  - Orange = pending (temporary highlight)
- ✏️ Reserve ranges or quantities of codes per client
- 🔐 Release codes securely with password authorization
- 🧾 Edit and add client details
- 🧠 Session tracking and locking to prevent multi-user conflicts
- 📆 View and filter full action history (by date, user, client, etc.)
- 👥 Login window with role-based access (`full`, `limited`, `view`)
- 💾 Excel auto-updating: works with `clients.xlsx` and `history.xlsx`
- 🪪 Dedicated tab for programming magnetic card fields

---

## 🛠️ Tech Stack

- Python 3.10+
- Tkinter (GUI)
- pandas, openpyxl
- Excel-based database (no SQL required)
- Role-based authentication via `users.xlsx`


