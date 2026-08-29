# Hamed AI — Koyeb Free deployment

Koyeb can deploy this public GitHub repository directly as a Web Service. The repository now has a cloud entrypoint and a Dockerfile that binds to `0.0.0.0:8000`.

## Control-panel deployment

1. Open the Koyeb control panel.
2. Choose **Create Web Service** → **GitHub**.
3. Select `aboaita202020-debug/hamed`, branch `main`.
4. Choose **Dockerfile** as the builder, or Buildpack with run command `python cloud_server.py`.
5. Expose HTTP port `8000` and route `/` to port `8000`.
6. Keep the Free/Nano instance for initial testing.
7. Add secrets only in Koyeb Environment Variables; never commit them to GitHub.

## Environment variables

For the free local/cloud smoke test, none are required. Optional integrations use:

- `OPENAI_API_KEY`
- `OPENAI_REALTIME_MODEL`
- `OPENAI_REALTIME_URL`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `PUBLIC_BASE_URL`

Do not paste real values into this file.

## Health checks

After deployment, open:

- `/` — service status
- `/health` — health and integration configuration status
- `/health/voice` — voice runtime health when the voice module is loaded

## Important limitation

Koyeb Free is intended for testing/hobby use. Free Instances have limited compute and scale to zero after one hour without traffic. This is suitable for validating Hamed before paying for production infrastructure, but it is not a guarantee of 24/7 voice availability.

## Koyeb CLI alternative

Koyeb's current CLI supports GitHub deployments. Example shape:

```bash
koyeb app init hamed/hamed \
  --git "github.com/aboaita202020-debug/hamed" \
  --git-branch "main" \
  --git-builder "docker" \
  --ports "8000:http" \
  --routes "/:8000"
```

Use the control panel if the CLI is not installed.
