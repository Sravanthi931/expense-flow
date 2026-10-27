# ExpenseFlow deployment

Streamlit embeds the existing React frontend at
`https://expense-flow-thhg.vercel.app`. It does not host the Spring Boot API or
MySQL database. Registration and all data-backed features need all three
services to be online and connected.

## 1. Host the MySQL database

Create a managed MySQL database with a public/TLS connection available to your
backend host. Create a database/schema named `expenseflow` and a database user
with permissions on that schema. Keep its hostname, port, username, and password
private. Do not use `localhost` for the hosted database URL.

## 2. Deploy the Spring Boot API on Render

1. Push the repository to GitHub and create a Render Blueprint from the root
   `render.yaml`, or create a Docker web service manually.
2. The Docker service uses `backend/Dockerfile`.
3. Set these environment variables in the backend service:
   - `SPRING_DATASOURCE_URL`: JDBC URL for the hosted MySQL database, such as
     `jdbc:mysql://DB_HOST:3306/expenseflow?useSSL=true`.
   - `SPRING_DATASOURCE_USERNAME`: the database user.
   - `SPRING_DATASOURCE_PASSWORD`: the database password.
   - `APP_JWT_SECRET`: a private Base64-encoded random key of at least 32 bytes.
   - `APP_CORS_ALLOWED_ORIGINS`: `https://expense-flow-thhg.vercel.app`
4. Wait for the backend deployment to succeed and copy its public HTTPS URL.

Do not put credentials in Git, chat, or frontend environment variables. Set them
only in the backend host's private environment settings.

## 3. Connect the Vercel frontend to the API

In the Vercel project settings, add the production environment variable
`VITE_API_BASE_URL` with the backend public URL and `/api` suffix, for example
`https://YOUR-BACKEND.onrender.com/api`. Redeploy the frontend after saving it.

The application reads this URL when Vite builds the frontend. The backend CORS
origin must exactly match the frontend origin, without a trailing slash.

## 4. Refresh Streamlit

Push the changed files to GitHub and reboot/redeploy the Streamlit app. It embeds
the React frontend; after the API and database are configured, test registration
on the React app and then through Streamlit.

The Vite development proxy remains the default when `VITE_API_BASE_URL` is
unset. In production, a missing API URL will send requests to the frontend host
and registration will fail.
