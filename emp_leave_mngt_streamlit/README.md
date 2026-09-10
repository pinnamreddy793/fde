# Employee Leave Management System

Streamlit implementation of the supplied flow diagram.

## Features
1. Register employee
2. View employees
3. Search employee
4. Apply for leave
5. Check leave balance
6. View leave requests
7. Save records to JSON
8. Export leave records to CSV
9. Exit

## Leave validation
- Start date cannot be after end date.
- Leave duration is calculated inclusively.
- A request is rejected when requested days exceed the employee's remaining balance.
- Approved requests reduce the employee's JSON leave balance.
- Leave requests are persisted in `employees.json`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
streamlit run app.py
```

The app opens in the browser at the Streamlit local URL.
