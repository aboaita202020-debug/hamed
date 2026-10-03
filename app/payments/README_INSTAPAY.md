# InstaPay payment option

Hamed now supports InstaPay as an additional Egypt/EGP payment option alongside Paymob and Vodafone Cash.

## Safety

- Hamed never requests or stores a customer's InstaPay PIN or OTP.
- A customer message, screenshot, or claimed transfer is **not** sufficient to mark an order as paid.
- `PAID` requires an authenticated provider callback or an authorized manual verification workflow.
- No automatic spending is enabled by this adapter.

## Production setup

Configure the receiving InstaPay identifier and account name through deployment secrets/configuration. Do not commit financial credentials to GitHub.
