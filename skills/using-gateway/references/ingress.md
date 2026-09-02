# Domains, TLS, Routes, and verification

Use this reference after the application target exists or when the request is specifically about Gateway ingress.

## Domain placement

Find or create the Domain on the Ingress Node that will serve the Route. A registered Domain and every Route using it must remain on the same compatible Ingress Node. Inspect existing DNS records before managed DNS writes. Never overwrite, adopt, or delete conflicting DNS without explicit user intent.

For external DNS, return the exact record change and wait for the user or provider. For Gateway-managed DNS, use the appropriate connector tools and re-check DNS after mutation.

## TLS

Reuse a compatible ready certificate when appropriate. Otherwise choose the supported ACME path:

- HTTP-01 requires the Domain to resolve to the assigned online Ingress Node with public port 80 reachable.
- Managed DNS-01 requires a matching connector and zone.
- Manual DNS-01 requires the user to create the returned TXT record before verification continues.

Use the SSL certificate identity expected by Routes, not an unrelated internal PKI certificate. Issuance is complete only when Gateway reports the certificate ready.

## Route targets

Use stable targets:

- standalone Container: Docker Node, stable Container name, and application port;
- Compose service: Docker Node, Compose Project, service identity, and application port;
- blue/green Deployment: Docker Node, Deployment identity, and application port;
- Pages: Pages Project and ready mutable Tag;
- manual upstream: explicit host, port, and scheme.

Enable WebSockets, redirects, access lists, headers, caching, rate limits, maintenance, health checks, or advanced nginx configuration only when required. Do not convert an unrelated Route because its hostname looks similar.

## Verification

Verify in layers:

1. target resource is ready and reports expected health;
2. Route is applied on the expected Ingress Node;
3. Domain resolves to the assigned ingress;
4. TLS is valid for the hostname;
5. an external HTTP request returns the expected status and, when practical, recognizable content or health response.

Return a verified URL only after the relevant layers pass. If external verification is unavailable, name the internal layers that passed and state that public reachability was not tested.
