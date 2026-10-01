# Vodafone Cash for Hamed AI

Hamed now supports Vodafone Cash as a **manual/merchant-wallet payment option** for Egypt.

## Customer flow

1. Hamed creates an order and a unique payment reference.
2. Customer receives the merchant Vodafone Cash wallet and the exact amount.
3. Customer transfers the amount using Vodafone Cash.
4. Customer sends the transaction/reference evidence through the configured support channel.
5. A trusted merchant-side verification confirms amount + reference.
6. Only then can the order move to `PAID`.

## Security rules

- Hamed must never request or store the customer's Vodafone Cash PIN or OTP.
- Never place wallet credentials, API secrets, or private keys in GitHub.
- Do not mark an order paid from a customer screenshot alone when a stronger merchant verification is available.
- Automated online Vodafone Cash checkout requires an approved merchant/API integration and provider webhook contract; this adapter deliberately does not pretend that a public consumer wallet transfer is an API.

## Environment

```text
HAMED_PAYMENTS_ENABLED=false
HAMED_VODAFONE_CASH_WALLET=<merchant-wallet-number>
HAMED_AUTO_SPENDING=false
```

Vodafone's official site confirms Vodafone Cash supports merchant/online payment flows, including wallet payment at participating partner sites. The exact automated merchant integration must be obtained through Vodafone's approved merchant channel.