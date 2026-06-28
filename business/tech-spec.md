## tech-spec.md  

### 1. Stack (language / framework / runtime)

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Swift 5.9** (Linux‑compatible) | Native performance, low‑latency, strong type safety; aligns with repo name and existing Swift ecosystem for networking. |
| **Web framework** | **Vapor 4** (async‑await, SwiftNIO) | Production‑grade, high‑throughput HTTP server; built‑in support for WebSockets & TLS; easy to containerise. |
| **AI inference** | **ONNX Runtime (C API) + Swift‑ONNX bindings** | Allows loading of pre‑trained path‑selection models (e.g., GNN, XGBoost) without heavy Python dependencies; runs on CPU/GPU. |
| **Database driver** | **Fluent 4** (ORM) with **PostgreSQL** backend | Declarative schema migrations, async queries, strong Swift typing. |
| **Message queue** | **NATS JetStream** | Ultra‑low latency pub/sub for real‑time pricing feeds and transaction events; simple to run on free tier. |
| **Container runtime** | **Docker** (multi‑stage build) | Guarantees reproducible builds; minimal Alpine‑based runtime image (~30 MB). |
| **Runtime** | **Linux (Ubuntu 22.04 LTS) on x86_64** | Broad cloud provider support; matches NATS & PostgreSQL official images. |

---

### 2. Hosting (free‑tier‑first, specific platforms)

| Component | Provider (Free‑Tier First) | Deployment Model | Cost‑Control Notes |
|-----------|----------------------------|------------------|--------------------|
| **API Service** | **Fly.io** (free‑tier: 3 VMs, 256 MiB RAM each) | Docker container, global edge locations | Auto‑scale to 1‑node; add paid plan only when >10 k RPS. |
| **PostgreSQL** | **Supabase** (free tier: 500 MB, 2 GB bandwidth) | Managed PostgreSQL 13 | Enable read‑replica on Supabase Pro only if >5 k QPS. |
| **NATS JetStream** | **Render.com** (free tier: 1 GB RAM, 1 CPU) | Docker container, private network | Use Render’s “Private Service” to keep traffic internal. |
| **Model Store** | **GitHub Packages (container registry)** | Store ONNX model artifacts as OCI images | Pull at startup; cache in Fly.io volume. |
| **Observability** | **Grafana Cloud Free** (metrics & logs) + **OpenTelemetry Collector** | SaaS endpoint; send via HTTPS | Retain 7‑day retention; upgrade only if >10 M data points/mo. |
| **CI/CD** | **GitHub Actions** (free minutes for public repo) | Build, test, push Docker image | Use self‑hosted runner on Render free tier for heavy model conversion. |

---

### 3. Data Model  

| Table / Collection | Primary Key | Key Fields | Description |
|--------------------|-------------|------------|-------------|
| **routes** | `route_id` (UUID) | `source_currency`, `dest_currency`, `provider_ids` (array), `base_fee`, `base_latency_ms`, `model_score` (float) | Cached routing options for a given currency pair. |
| **providers** | `provider_id` (UUID) | `name`, `api_endpoint`, `auth_type`, `fee_structure`, `latency_profile`, `status` (enum) | External payment rails (SWIFT, SEPA, Ripple, etc.). |
| **transactions** | `tx_id` (UUID) | `client_id`, `route_id`, `amount`, `currency`, `status` (enum), `created_at`, `completed_at`, `fee_charged`, `latency_ms` | Audit trail for every routed payment. |
| **clients** | `client_id` (UUID) | `name`, `api_key`, `quota_daily`, `allowed_countries` (array) | API consumer metadata. |
| **pricing_feeds** | `feed_id` (UUID) | `provider_id`, `currency_pair`, `fee`, `estimated_latency_ms`, `timestamp` | Real‑time feed used by AI model to recompute scores. |
| **model_metadata** | `model_id` (UUID) | `version`, `trained_at`, `accuracy`, `features_used` (array) | Tracks which AI model is active. |

*All timestamps stored as UTC ISO‑8601. Soft‑delete via `deleted_at` nullable column.*

---

### 4. API Surface  

| Method | Path | Purpose | Request Body (JSON) | Response (JSON) |
|--------|------|---------|---------------------|-----------------|
| **POST** | `/v1/route` | Compute optimal route for a payment request. | `{ "client_id": "...", "source_currency": "USD", "dest_currency": "JPY", "amount": 125000, "asset_type": "fiat|crypto" }` | `{ "route_id": "...", "provider_sequence": ["providerA","providerB"], "total_fee": 12.34, "estimated_latency_ms": 420, "model_version": "v1.2.3" }` |
| **GET** | `/v1/route/{route_id}` | Retrieve cached route details. | – | Same payload as above + `created_at`. |
| **POST** | `/v1/transaction` | Submit a payment for execution on the selected route. | `{ "route_id": "...", "client_reference": "INV-12345", "beneficiary": { "name": "...", "account": "..." } }` | `{ "tx_id": "...", "status": "queued", "estimated_completion": "2026-06-18T14:32:00Z" }` |
| **GET** | `/v1/transaction/{tx_id}` | Poll transaction status. | – | `{ "tx_id":"...", "status":"completed|failed|pending", "fee_charged":12.34, "latency_ms": 438, "error_code": null }` |
| **GET** | `/v1/providers` | List all enabled payment providers with health status. | – | `[ { "provider_id":"...", "name":"...", "status":"online", "avg_latency_ms": 78 } ]` |
| **POST** | `/v1/clients` | Register a new API client (admin only). | `{ "name":"Acme Corp", "quota_daily":1000, "allowed_countries":["US","JP"] }` | `{ "client_id":"...", "api_key":"<secret>" }` |
| **GET** | `/v1/healthz` | Liveness / readiness probe. | – | `{ "status":"ok", "uptime_seconds": 12345 }` |
| **GET** | `/v1/metrics` | Prometheus‑compatible metrics endpoint (internal). | – | *plain‑text metrics* |

*All mutating endpoints require **Bearer** token (API key) with `x-api-key` header.*

---

### 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | API‑Key (UUID) issued per client; sent as `Authorization: Bearer <key>`; validated against `clients.api_key` (hashed with Argon2). |
| **Transport Security** | Enforced TLS 1.3 via Fly.io edge; internal services communicate over mTLS (self‑signed certs rotated weekly). |
| **Secrets Management** | - API keys stored hashed.<br>- Database credentials & NATS token stored in **Fly.io Secrets** (encrypted at rest).<br>- ONNX model files pulled from private GitHub Packages using a **GitHub Actions** token. |
| **IAM / RBAC** | Simple role enum on `clients.role` (`admin`, `partner`). Middleware checks role for admin‑only routes (`/v1/clients`). |
| **Input Validation** | Vapor’s `Content` decoders + custom validators (e.g., amount > 0, currency ISO‑4217). |
| **Rate Limiting** | NATS‑backed token bucket per `client_id` (default 100 req/s, configurable via `quota_daily`). |
| **Audit Logging** | Every request logs `client_id`, endpoint, request hash, response status, and latency to Grafana Loki. |
| **Compliance** | Data at rest encrypted (PostgreSQL Transparent Data Encryption); GDPR‑compliant deletion via `deleted_at`. |

---

### 6. Observability  

| Signal | Tooling | Export |
|--------|---------|--------|
| **Logs** | `swift-log` → OpenTelemetry Collector → **Grafana Loki** (free tier) | Structured JSON (`timestamp`, `level`, `request_id`, `client_id`, `msg`). |
| **Metrics** | `Prometheus` client library (Swift) → `/v1/metrics` endpoint → **Grafana Cloud** | Key metrics: `request_duration_seconds`, `route_selection_latency_ms`, `tx_success_total`, `tx_failure_total`, `db_query_time_seconds`. |
| **Traces** | **OpenTelemetry Swift** instrumentation (HTTP, DB, NATS) → Collector → **Grafana Tempo** (free) | End‑to‑end trace of a payment request through route selection → provider calls. |
| **Health** | `/v1/healthz` + **Fly.io health checks** | Alerts on 5xx rate > 1% via Grafana Alerting. |
| **Dashboards** | Pre‑built Grafana dashboards for latency heatmaps, fee distribution, model score drift. | Auto‑refresh every 30 s. |

---

### 7. Build / CI  

| Stage | Tool | Steps |
|-------|------|-------|
| **Lint / Format** | **SwiftLint** (via GitHub Action) | `swiftlint lint --strict` |
| **Unit Tests** | **XCTest** | `swift test --parallel` (target coverage ≥ 80%). |
| **Integration Tests** | Docker‑compose (Postgres + NATS + API) | Spin up services, run `swift test --filter Integration`. |
| **Model Validation** | Python script (runs on self‑hosted runner) | Load ONNX model, run sanity check on sample pricing feed, output checksum. |
| **Docker Build** | **Docker** (multi‑stage) | Stage 1: `swift build -c release`; Stage 2: copy binary + runtime libs into `alpine:3.19` base. |
| **Security Scan** | **Trivy** | Scan final image for CVEs; fail on > Critical. |
| **Publish** | **GitHub Container Registry** | Tag `ghcr.io/arkashira/swift-route:<git-sha>`; also push `latest` on main merge. |
| **Deploy** | **Fly.io Deploy Action** | `flyctl deploy --image ghcr.io/...` on successful push to `main`. |
| **Rollback** | Fly.io `release` history + `flyctl rollback <release-id>` | Automated rollback on health‑check failure (>2 consecutive failures). |

*All pipelines run on GitHub Actions free tier for public repos; heavy model conversion steps off‑loaded to a self‑hosted runner on Render (free tier).*

---  

*End of `tech-spec.md`.*