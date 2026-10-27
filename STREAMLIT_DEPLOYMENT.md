# ExpenseFlow on Streamlit

The Streamlit page embeds the existing React application hosted at
`https://expense-flow-thhg.vercel.app`. This keeps the original login,
registration, dashboard, and application routes in the React app instead of
reimplementing them as a reduced Streamlit-only analytics page.

## Deploy

1. Push the updated `streamlit_app.py`, `requirements.txt`, and this guide to the
   GitHub branch connected to Streamlit Community Cloud.
2. In Streamlit Community Cloud, open the deployed app and choose **Manage app**
   then **Reboot app** (or redeploy the latest commit).
3. Open the Streamlit app URL. Its page embeds the full React app and also
   provides a button to open the React app in a new tab.

The frontend URL is configured in `streamlit_app.py`.

The embedded React application still depends on its Spring Boot API and
production database. Ensure the React deployment is built with its production
API URL and the backend allows the React frontend origin in CORS. Streamlit
does not host or replace those services.
