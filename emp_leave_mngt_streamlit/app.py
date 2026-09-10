import csv
import json
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path("employees.json")
CSV_FILE = Path("leave_records.csv")


# -----------------------------
# Persistence helpers
# -----------------------------
def load_employees():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        st.error("Unable to read employees.json.")
        return []


def save_employees(employees):
    DATA_FILE.write_text(json.dumps(employees, indent=2), encoding="utf-8")


def find_employee(employees, employee_id):
    return next(
        (e for e in employees if e["employee_id"].lower() == employee_id.lower()),
        None,
    )


def export_csv(employees):
    rows = []
    for emp in employees:
        for req in emp.get("leave_requests", []):
            rows.append({
                "employee_id": emp["employee_id"],
                "employee_name": emp["name"],
                "department": emp.get("department", ""),
                "leave_type": req["leave_type"],
                "start_date": req["start_date"],
                "end_date": req["end_date"],
                "days": req["days"],
                "status": req["status"],
                "reason": req.get("reason", ""),
            })

    columns = [
        "employee_id", "employee_name", "department", "leave_type",
        "start_date", "end_date", "days", "status", "reason"
    ]
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(CSV_FILE, index=False)
    return df


# -----------------------------
# Streamlit setup
# -----------------------------
st.set_page_config(
    page_title="Employee Leave Management",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Employee Leave Management System")
st.caption("Menu-driven application with JSON persistence and CSV export.")

if "employees" not in st.session_state:
    st.session_state.employees = load_employees()

employees = st.session_state.employees

# -----------------------------
# Sidebar = Main Menu
# -----------------------------
st.sidebar.header("Main Menu")
option = st.sidebar.radio(
    "Select an option",
    [
        "1. Register Employee",
        "2. View Employees",
        "3. Search Employee",
        "4. Apply for Leave",
        "5. Check Leave Balance",
        "6. View Leave Requests",
        "7. Save Records (JSON)",
        "8. Export Records (CSV)",
        "9. Exit",
    ],
)

# -----------------------------
# 1. Register Employee
# -----------------------------
if option.startswith("1."):
    st.header("1. Register Employee")

    with st.form("register_employee"):
        employee_id = st.text_input("Employee ID")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
        balance = st.number_input(
            "Initial Leave Balance (days)",
            min_value=0,
            max_value=365,
            value=20,
            step=1,
        )
        submitted = st.form_submit_button("Register Employee")

    if submitted:
        employee_id = employee_id.strip()

        if not employee_id or not name.strip():
            st.warning("Employee ID and name are required.")
        elif find_employee(employees, employee_id):
            st.error(f"Employee {employee_id} already exists.")
        else:
            employees.append({
                "employee_id": employee_id,
                "name": name.strip(),
                "email": email.strip(),
                "department": department.strip(),
                "leave_balance": int(balance),
                "leave_requests": [],
            })
            save_employees(employees)
            st.success(f"Employee {employee_id} registered successfully.")

# -----------------------------
# 2. View Employees
# -----------------------------
elif option.startswith("2."):
    st.header("2. View Employees")

    if not employees:
        st.info("No employees registered.")
    else:
        rows = [
            {
                "Employee ID": e["employee_id"],
                "Name": e["name"],
                "Email": e.get("email", ""),
                "Department": e.get("department", ""),
                "Leave Balance": e.get("leave_balance", 0),
            }
            for e in employees
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# -----------------------------
# 3. Search Employee
# -----------------------------
elif option.startswith("3."):
    st.header("3. Search Employee")

    search = st.text_input("Enter Employee ID or name").strip().lower()

    if search:
        matches = [
            e for e in employees
            if search in e["employee_id"].lower()
            or search in e["name"].lower()
        ]

        if matches:
            for e in matches:
                st.success(
                    f"**{e['employee_id']} — {e['name']}** | "
                    f"{e.get('department', 'N/A')} | "
                    f"Leave balance: **{e.get('leave_balance', 0)} days**"
                )
        else:
            st.warning("No matching employee found.")

# -----------------------------
# 4. Apply for Leave
# -----------------------------
elif option.startswith("4."):
    st.header("4. Apply for Leave")

    employee_id = st.text_input("Employee ID").strip()
    employee = find_employee(employees, employee_id) if employee_id else None

    if employee:
        st.info(
            f"{employee['name']} — Current leave balance: "
            f"**{employee.get('leave_balance', 0)} days**"
        )

        with st.form("leave_application"):
            leave_type = st.selectbox(
                "Leave Type", ["Annual", "Sick", "Personal", "Other"]
            )
            start_date = st.date_input("Start Date", value=date.today())
            end_date = st.date_input("End Date", value=date.today())
            reason = st.text_area("Reason (optional)")
            submitted = st.form_submit_button("Submit Leave Request")

        if submitted:
            if end_date < start_date:
                st.error("End date cannot be before start date.")
            else:
                requested_days = (end_date - start_date).days + 1
                balance = int(employee.get("leave_balance", 0))

                # Leave balance validation
                if requested_days <= 0:
                    st.error("Leave duration must be at least one day.")
                elif requested_days > balance:
                    st.error(
                        f"Insufficient leave balance. You requested "
                        f"{requested_days} day(s), but only {balance} day(s) remain."
                    )
                else:
                    request = {
                        "leave_type": leave_type,
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "days": requested_days,
                        "status": "Approved",
                        "reason": reason.strip(),
                    }

                    employee.setdefault("leave_requests", []).append(request)
                    employee["leave_balance"] = balance - requested_days

                    save_employees(employees)
                    st.success(
                        f"Leave request submitted successfully for "
                        f"{requested_days} day(s). Remaining balance: "
                        f"**{employee['leave_balance']} days**."
                    )
    elif employee_id:
        st.warning("Employee not found. Please register the employee first.")

# -----------------------------
# 5. Check Leave Balance
# -----------------------------
elif option.startswith("5."):
    st.header("5. Check Leave Balance")

    employee_id = st.text_input("Employee ID").strip()

    if employee_id:
        employee = find_employee(employees, employee_id)
        if employee:
            balance = employee.get("leave_balance", 0)
            st.metric("Remaining Leave Days", balance)
        else:
            st.warning("Employee not found.")

# -----------------------------
# 6. View Leave Requests
# -----------------------------
elif option.startswith("6."):
    st.header("6. View Leave Requests")

    employee_id = st.text_input(
        "Employee ID (leave blank to view all requests)"
    ).strip()

    selected = (
        [find_employee(employees, employee_id)]
        if employee_id and find_employee(employees, employee_id)
        else employees if not employee_id
        else []
    )

    rows = []
    for emp in selected:
        for req in emp.get("leave_requests", []):
            rows.append({
                "Employee ID": emp["employee_id"],
                "Employee Name": emp["name"],
                "Leave Type": req["leave_type"],
                "Start Date": req["start_date"],
                "End Date": req["end_date"],
                "Days": req["days"],
                "Status": req["status"],
                "Reason": req.get("reason", ""),
            })

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    elif employee_id:
        st.info("No leave requests found for this employee.")
    else:
        st.info("No leave requests have been submitted.")

# -----------------------------
# 7. Save Records (JSON)
# -----------------------------
elif option.startswith("7."):
    st.header("7. Save Records (JSON)")

    save_employees(employees)
    st.success(f"Employee and leave records saved to `{DATA_FILE}`.")

    st.download_button(
        "Download employees.json",
        data=json.dumps(employees, indent=2),
        file_name="employees.json",
        mime="application/json",
    )

# -----------------------------
# 8. Export Records (CSV)
# -----------------------------
elif option.startswith("8."):
    st.header("8. Export Records (CSV)")

    df = export_csv(employees)

    if df.empty:
        st.info("No leave records available to export.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download leave_records.csv",
            data=df.to_csv(index=False),
            file_name="leave_records.csv",
            mime="text/csv",
        )
        st.success("CSV export is ready.")

# -----------------------------
# 9. Exit
# -----------------------------
elif option.startswith("9."):
    st.header("9. Exit")
    save_employees(employees)
    st.success("Data saved successfully. You can close the application.")
