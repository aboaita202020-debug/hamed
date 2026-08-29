# Hamed AI on Northflank Free

Northflank currently offers a Developer Sandbox free tier with 2 services, 2 jobs, and 1 addon. Northflank documentation says services can run continuously, and its 2026 deployment guide states the free tier can be used without a credit card for the sandbox. Verify current account eligibility during signup.

## Deploy

1. Create a Northflank account: https://app.northflank.com/
2. Create a project on **Northflank Cloud**.
3. Link your GitHub account and select `aboaita202020-debug/hamed`.
4. Create a **Combined service**.
5. Select the repository and branch `main`.
6. Select **Dockerfile** as the build method. The repository root contains `Dockerfile`.
7. Expose public port `8000` as HTTP.
8. Add runtime environment variables only in Northflank's secret/environment UI. Never commit real secrets.
9. Deploy.

## Runtime variables

For the free server-only test, Hamed needs no paid integration keys. Keep these disabled until needed:

- `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`

Recommended runtime values:

- `HAMED_HOST=0.0.0.0`
- `HAMED_PORT=8000`
- `APP_ENV=production`

## Health check

Northflank should be able to reach:

`GET /health`

Expected result:

```json
{"status":"ok","voice":"disabled","paid_integrations":"disabled"}
```

## Important

The free Northflank tier is suitable for development, testing and a first live deployment. AI API usage and telephone minutes are separate costs and are not made free by the server plan.
