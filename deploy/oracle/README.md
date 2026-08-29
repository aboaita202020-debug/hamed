# Hamed AI — Oracle Cloud Always Free deployment

## Goal
Run Hamed 24/7 in the cloud so it does not depend on the owner's phone or PC being online.

## Bootstrap
1. Create an eligible Oracle Cloud Always Free Ubuntu VM.
2. SSH into the VM as an administrator.
3. Run `bash deploy/oracle/cloud-init.sh` from a checkout of this repository.
4. Copy `deploy/oracle/hamed.env.example` to `/etc/hamed/hamed.env`.
5. Add secrets only on the VM and set file permissions to `chmod 600 /etc/hamed/hamed.env`.
6. Restart with `sudo systemctl restart hamed`.

## Free-first behavior
The example configuration keeps `PAID_SERVICES_ENABLED=false` and `VOICE_ENABLED=false`. This allows local/cloud development without silently creating paid usage. Enable paid voice only after the owner has deliberately configured a provider and budget.

## Production requirements
- Public HTTPS endpoint for inbound webhooks/media streams.
- Firewall rules limited to required ports.
- Valid provider credentials stored outside Git.
- Backups for persistent data.
- Monitoring and log rotation.

The VM itself can remain online while the owner's phone and computer are offline. External phone calls still depend on the selected telecom/voice provider and are not made free by the VM.
