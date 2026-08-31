# Run Hamed for free

This repository includes `.github/workflows/run-hamed.yml`.

1. Open the Actions tab.
2. Select **Hamed AI - Free Runner**.
3. Click **Run workflow**.
4. Select branch `feat/hamed-phase2-core`.
5. Click **Run workflow**.

The workflow installs dependencies, compiles the Python source, and runs tests when the repository has a `tests/` directory.

Important: GitHub Actions is a job runner, not a permanent 24/7 Telegram hosting service. A workflow exits after the job. For a continuously running Telegram bot, Hamed needs a machine that stays online (for example a computer you already own using a self-hosted runner) or a suitable always-on hosting service.

Never commit Telegram, Google, or AI provider secrets. Store them in the runtime environment or repository Actions secrets.
