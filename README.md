# Solana Cord

Implementation of Solana's JSON RPC API, wrapped for discord bots.

94421759 245759 1630521412 1630390553 0.5688865740740741

### Endpoints
- https://api.mainnet-beta.solana.com - Solana-hosted api node cluster, backed by a load balancer; rate-limited
- https://solana-api.projectserum.com - Project Serum-hosted api node

### Rate Limits
- Maximum number of requests per 10 seconds per IP: 100
- Maximum number of requests per 10 seconds per IP for a   single RPC: 40
- Maximum concurrent connections per IP: 40
- Maximum connection rate per 10 seconds per IP: 40
- Maximum amount of data per 30 second: 100 MB
