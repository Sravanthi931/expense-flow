# Streamlit deployment

This repository now includes a separate Streamlit expense analytics companion.
It reads a CSV/TSV file uploaded by the visitor and runs in-memory analysis. It
does not replace or deploy the existing React frontend or Spring Boot API, and
does not need database credentials.

## Deploy on Streamlit Community Cloud

1. Push the repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and
   choose **Create app**.
3. Select the repository and branch, set **Main file path** to
   `streamlit_app.py`, then deploy.
4. After the build completes, copy the app URL from Streamlit. That is the
   shareable link; the link cannot be assigned before Streamlit creates the app.

Community Cloud installs dependencies from the root `requirements.txt`.

## Input data

Upload a comma- or tab-delimited file with `expense_date` and `amount` columns.
`date` is accepted in place of `expense_date`; `category` is optional. Optional
`description` and `notes` columns appear in the transaction table. Download the
CSV template from the app to see an example.

Uploaded data is analyzed in the app session and is not written to this
repository or database. Do not upload data you do not want processed by the
hosted Streamlit service.
