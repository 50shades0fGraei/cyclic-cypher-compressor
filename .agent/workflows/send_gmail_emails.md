---
description: Configure terminal email sending via Gmail using msmtp
---

## Prerequisites
1. Ensure you have a Gmail account with **App Password** enabled (recommended for security).
2. Install `msmtp` and `s-nail` (which provides the `mail` command) on your Arch Linux system.
   ```bash
   sudo pacman -Sy msmtp s-nail
   ```

## Steps
1. **Create msmtp configuration file**
   ```bash
   cat > ~/.msmtprc <<EOF
   # Set default values for all following accounts.
   defaults
   auth           on
   tls            on
   tls_trust_file /etc/ssl/certs/ca-certificates.crt
   logfile        ~/.msmtp.log

   # Gmail account
   account        gmail
   host           smtp.gmail.com
   port           587
   from           YOUR_EMAIL@gmail.com
   user           YOUR_EMAIL@gmail.com
   passwordeval   "gpg --quiet --for-your-eyes-only --no-tty -d ~/.gmail_app_password.gpg"
   # Alternatively, replace the line above with:
   # password       YOUR_APP_PASSWORD

   # Set a default account
   account default : gmail
   EOF
   chmod 600 ~/.msmtprc
   ```
   > **Note**: For security, store the app password encrypted with GPG and reference it via `passwordeval` as shown.

2. **Test sending a simple email**
   ```bash
   echo "Test email body" | mail -s "Test Subject" recipient@example.com
   ```
   Check `~/.msmtp.log` for any errors.

3. **Optional: Create a helper script** (e.g., `send_email.sh`)
   ```bash
   #!/usr/bin/env bash
   SUBJECT="$1"
   RECIPIENT="$2"
   shift 2
   BODY="$(cat)"
   echo "$BODY" | mail -s "$SUBJECT" "$RECIPIENT"
   ```
   Make it executable: `chmod +x send_email.sh`.

4. **Automate with cron or scripts** as needed.

## Troubleshooting
- Verify that less‑secure app access is disabled; use an **App Password** instead.
- Ensure the `msmtp` log (`~/.msmtp.log`) shows `250 OK` after sending.
- If authentication fails, re‑generate the app password and update the encrypted file.

---
