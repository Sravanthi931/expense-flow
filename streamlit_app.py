from __future__ import annotations

from io import StringIO

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ExpenseFlow Analytics",
    page_icon="📊",
    layout="wide",
)


REQUIRED_COLUMNS = {"amount", "expense_date"}


def read_expenses(file_bytes: bytes) -> tuple[pd.DataFrame, int]:
    """Read comma- or tab-delimited expense data from an uploaded file."""
    content = file_bytes.decode("utf-8-sig")
    frame = pd.read_csv(StringIO(content), sep=None, engine="python")
    frame.columns = [str(column).strip().lower() for column in frame.columns]

    if "date" in frame.columns and "expense_date" not in frame.columns:
        frame = frame.rename(columns={"date": "expense_date"})

    missing_columns = REQUIRED_COLUMNS - set(frame.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}.")

    if "category" not in frame.columns:
        frame["category"] = "Uncategorized"

    frame["expense_date"] = pd.to_datetime(frame["expense_date"], errors="coerce")
    frame["amount"] = pd.to_numeric(frame["amount"], errors="coerce")
    frame["category"] = frame["category"].fillna("Uncategorized").astype(str).str.strip()
    frame.loc[frame["category"] == "", "category"] = "Uncategorized"

    invalid_rows = int(frame[["expense_date", "amount"]].isna().any(axis=1).sum())
    return frame.dropna(subset=["expense_date", "amount"]), invalid_rows


st.title("ExpenseFlow Analytics")
st.caption(
    "Explore spending from an uploaded expense export. Amounts use the currency "
    "represented by your file."
)
st.info(
    "This is an optional Streamlit analytics companion. The existing React and "
    "Spring Boot application remains unchanged and is not hosted by this page."
)

template = pd.DataFrame(
    [
        {"expense_date": "2026-01-15", "amount": 25.50, "category": "Food", "description": "Lunch"},
        {"expense_date": "2026-01-20", "amount": 40.00, "category": "Transport", "description": "Bus pass"},
    ]
)
st.download_button(
    "Download CSV template",
    data=template.to_csv(index=False).encode("utf-8"),
    file_name="expenseflow_template.csv",
    mime="text/csv",
)

uploaded_file = st.file_uploader(
    "Upload expenses as CSV or TSV",
    type=["csv", "tsv", "txt"],
    help="Required columns: expense_date and amount. category is optional; date is also accepted.",
)

if uploaded_file is None:
    st.warning("Upload an expense export to see its analytics. Your file is processed in memory.")
    st.stop()

try:
    expenses, invalid_rows = read_expenses(uploaded_file.getvalue())
except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
    st.error(f"Could not read this expense file: {error}")
    st.stop()

if expenses.empty:
    st.warning("No rows with a valid date and numeric amount were found in this file.")
    st.stop()

if (expenses["amount"] < 0).any():
    st.caption("Negative amounts are included as credits/refunds.")

minimum_date = expenses["expense_date"].min().date()
maximum_date = expenses["expense_date"].max().date()
start_date = st.sidebar.date_input(
    "Start date",
    value=minimum_date,
    min_value=minimum_date,
    max_value=maximum_date,
)
end_date = st.sidebar.date_input(
    "End date",
    value=maximum_date,
    min_value=minimum_date,
    max_value=maximum_date,
)
if start_date > end_date:
    st.sidebar.error("Start date must be on or before end date.")
    st.stop()

categories = sorted(expenses["category"].unique())
selected_categories = st.sidebar.multiselect("Categories", categories, default=categories)

filtered = expenses[
    expenses["expense_date"].dt.date.between(start_date, end_date)
    & expenses["category"].isin(selected_categories)
].copy()

if filtered.empty:
    st.warning("No expenses match the selected date range and categories.")
    st.stop()

if invalid_rows:
    st.warning(f"{invalid_rows} row(s) with missing or invalid dates were excluded.")

filtered["month"] = filtered["expense_date"].dt.to_period("M").astype(str)
monthly = (
    filtered.groupby("month", as_index=False)
    .agg(total_spent=("amount", "sum"), transactions=("amount", "size"))
    .sort_values("month")
)
by_category = (
    filtered.groupby("category", as_index=False)
    .agg(total_spent=("amount", "sum"), transactions=("amount", "size"))
    .sort_values("total_spent", ascending=False)
)

total_spent = filtered["amount"].sum()
average_expense = filtered["amount"].mean()
top_category = by_category.iloc[0]["category"]

metric_columns = st.columns(4)
metric_columns[0].metric("Total spent", f"{total_spent:,.2f}")
metric_columns[1].metric("Transactions", f"{len(filtered):,}")
metric_columns[2].metric("Average expense", f"{average_expense:,.2f}")
metric_columns[3].metric("Top category", str(top_category))

monthly_chart, category_chart = st.columns(2)
with monthly_chart:
    st.subheader("Monthly spending")
    st.bar_chart(monthly.set_index("month")["total_spent"], y_label="Amount")
with category_chart:
    st.subheader("Spending by category")
    st.bar_chart(by_category.set_index("category")["total_spent"], y_label="Amount")

st.subheader("Filtered transactions")
visible_columns = [
    column
    for column in ("expense_date", "amount", "category", "description", "notes")
    if column in filtered.columns
]
st.dataframe(
    filtered.sort_values("expense_date", ascending=False)[visible_columns],
    width="stretch",
    hide_index=True,
)

export = filtered.drop(columns=["month"], errors="ignore").to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered expenses",
    data=export,
    file_name="expenseflow_filtered.csv",
    mime="text/csv",
)
