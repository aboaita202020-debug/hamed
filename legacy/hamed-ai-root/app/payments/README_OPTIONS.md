# Egypt payment menu

Hamed presents three payment choices for Egypt/EGP:

1. Paymob — hosted checkout/card flow; automated confirmation is supported when the configured provider callback is verified.
2. Vodafone Cash — customer wallet transfer; no PIN/OTP is requested or stored. Automatic confirmation requires an approved provider integration or authorized verification.
3. InstaPay — customer bank transfer; no PIN/OTP is requested or stored. A customer screenshot/message is not treated as proof of payment; use authenticated provider confirmation or authorized verification.

All provider credentials belong in deployment secrets/environment variables and must never be committed to the repository.
