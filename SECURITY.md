# Security Documentation

## OWASP Top 10 — Finance OS

### 1. Broken Access Control
All endpoints require JWT authentication via Bearer token.
Users can only access their own data — every query filters by user_id.
Role-based access control implemented via user.role field.

### 2. Cryptographic Failures
Passwords hashed using bcrypt with salt rounds.
JWT tokens signed with HS256 algorithm using a strong random secret key.
All secrets stored in environment variables — never in code or Git.
HTTPS enforced in production via Railway and Vercel.

### 3. Injection
All database queries use SQLAlchemy ORM with parameterized queries.
No raw SQL strings constructed from user input anywhere in the codebase.
All API inputs validated with Pydantic schemas before reaching the database.

### 4. Insecure Design
Authentication requires email verification of existing user before token issuance.
Login errors return identical messages regardless of which field is wrong.
This prevents username enumeration attacks.

### 5. Security Misconfiguration
CORS restricted to known origins only.
Environment variables used for all configuration.
No debug mode in production — ENVIRONMENT variable controls this.
Docker images use minimal base images with no unnecessary tools.

### 6. Vulnerable and Outdated Components
All dependencies pinned in requirements.txt and package.json.
Regular dependency updates via pip and npm.

### 7. Identification and Authentication Failures
JWT tokens expire after 30 minutes.
Rate limiting on auth endpoints — 5 attempts per minute per IP.
Passwords never stored in plain text or returned in any API response.

### 8. Software and Data Integrity Failures
All code changes go through pull requests with CI verification.
Branch protection prevents direct pushes to main.
GitHub Actions pipeline validates build before deployment.

### 9. Security Logging and Monitoring
Every request logged with method, path, status code, and duration.
Failed authentication attempts logged.
Sentry configured for error monitoring in production.

### 10. Server-Side Request Forgery
No server-side HTTP requests to user-supplied URLs.
External API calls limited to yfinance for CSPX price data only.