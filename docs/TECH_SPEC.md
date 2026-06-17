# TECH_SPEC.md

## Swift‑Route – Technical Specification

---

## 1. Overview

Swift‑Route is a low‑latency, cost‑optimized payment routing platform that leverages AI‑driven path selection to accelerate cross‑border and digital‑asset transactions for banks and payment providers. The system is designed for high throughput, fault‑tolerance, and compliance with financial regulations.

---

## 2. Architecture

```
┌──────────────────────┐
│  Client / API Gateway│
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  Request Router      │
│  (FastAPI + uvicorn) │
└───────┬───────┬──────┘
        │       │
        ▼       ▼
┌──────────────┐ ┌───────────────────────┐
│  AI‑Selector │ │  Liquidity Provider    │
│  (vLLM)      │ │  (REST/GRPC)           │
└───────┬──────┘ └──────────────┬────────┘
        │                     │
        ▼                     ▼
┌──────────────────────┐ ┌───────────────────────┐
│  Transaction Engine  │ │  Settlement Engine     │
│  (async Rust)        │ │  (async Rust)          │
└───────┬───────┬──────┘ └───────┬───────┬──────┘
        │       │              │       │
        ▼       ▼              ▼       ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  DB (PostgreSQL)│ │  Cache (Redis)│ │  Metrics (Prometheus)│ │  Logs (ELK) │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### 2.1. Components

| Layer | Component | Technology | Responsibility |
|-------|-----------|------------|----------------|
| **API** | Request Router | FastAPI + uvicorn | Exposes REST endpoints, authentication, rate‑limiting |
| **AI** | Path Selector | vLLM (LLM inference) | Generates optimal routing paths based on cost, latency, FX rates |
| **Liquidity** | Provider Connector | GRPC / REST | Communicates with external liquidity providers |
| **Engine** | Transaction Engine | Rust async | Validates, signs, and forwards payment instructions |
| **Engine** | Settlement Engine | Rust async | Handles post‑settlement reconciliation |
| **Storage** | PostgreSQL | SQL | Persistent state (transactions, routing tables, audit logs) |
| **Cache** | Redis | Key‑value | Session cache, rate‑limit counters, hot routing data |
| **Observability** | Prometheus + Grafana | Metrics | Latency, throughput, error rates |
| **Observability** | ELK (Elastic + Logstash + Kibana) | Logs | Centralized logging, alerting |

---

## 3. Data Model

```sql
-- transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    source_account TEXT NOT NULL,
    destination_account TEXT NOT NULL,
    amount NUMERIC(20, 8) NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- routing_paths
CREATE TABLE routing_paths (
    id UUID PRIMARY KEY,
    transaction_id UUID REFERENCES transactions(id),
    provider_id TEXT NOT NULL,
    path TEXT NOT NULL,          -- JSON array of hops
    cost NUMERIC(20, 8) NOT NULL,
    latency_ms INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- providers
CREATE TABLE providers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    auth_token TEXT NOT NULL,
    status TEXT NOT NULL
);

-- audit_log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    transaction_id UUID,
    event TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

---

## 4. Key APIs / Interfaces

### 4.1. REST Endpoints (FastAPI)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| POST | `/api/v1/transactions` | Create a new payment request | `TransactionCreate` | `TransactionResponse` |
| GET | `/api/v1/transactions/{id}` | Get transaction status | N/A | `TransactionResponse` |
| GET | `/api/v1/providers` | List available liquidity providers | N/A | `ProviderList` |
| POST | `/api/v1/providers/{id}/health` | Health check | N/A | `HealthStatus` |

### 4.2. GRPC Service (Liquidity Connector)

```
service LiquidityProvider {
  rpc Quote(QuoteRequest) returns (QuoteResponse);
  rpc Execute(ExecuteRequest) returns (ExecuteResponse);
}
```

### 4.3. Internal Interfaces

| Interface | Language | Purpose |
|-----------|----------|---------|
| `PathSelector` | Rust | `fn select_paths(request: &Transaction) -> Vec<Path>` |
| `TransactionValidator` | Rust | `fn validate(&Transaction) -> Result<()>` |
| `SettlementProcessor` | Rust | `fn settle(&Transaction) -> Result<()>` |

---

## 5. Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API** | FastAPI (Python 3.11) | Modern async framework, excellent typing |
| **AI** | vLLM (Python) | Production‑grade LLM inference, GPU‑optimized |
| **Engine** | Rust 1.75 | Zero‑cost abstractions, high performance |
| **Database** | PostgreSQL 15 | ACID compliance, JSONB support |
| **Cache** | Redis 7 | Low‑latency key‑value store |
| **Observability** | Prometheus + Grafana | Metrics collection, dashboards |
| **Logging** | Elastic Stack | Centralized log aggregation |
| **Containerization** | Docker + Docker‑Compose | Consistent dev / prod environments |
| **CI/CD** | GitHub Actions | Automated tests, linting, image build |
| **Secrets** | Vault (HashiCorp) | Secure storage for API keys |

---

## 6. Dependencies

| Package | Version | Notes |
|---------|---------|-------|
| `fastapi` | ^0.110.0 | Web framework |
| `uvicorn` | ^0.29.0 | ASGI server |
| `vllm` | ^0.5.0 | LLM inference |
| `tokio` | ^1.35 | Async runtime for Rust |
| `sqlx` | ^0.7 | Async PostgreSQL driver |
| `redis` | ^0.27 | Rust Redis client |
| `serde` | ^1.0 | Serialization |
| `prost` | ^0.12 | GRPC codegen |
| `prometheus` | ^0.13 | Metrics |
| `log` | ^0.4 | Logging |
| `dotenv` | ^0.15 | Environment variables |

All dependencies are pinned in `Cargo.toml` (Rust) and `requirements.txt` (Python).

---

## 7. Deployment

### 7.1. Architecture Diagram

```
[Client] ──► [Ingress (NGINX)] ──► [API Gateway (FastAPI)] ──►
           ├─► [AI Selector (vLLM)] ──► [Redis Cache]
           ├─► [Transaction Engine (Rust)]
           └─► [Settlement Engine (Rust)]
           │
           ├─► [PostgreSQL] (replicated)
           ├─► [Redis] (replicated)
           ├─► [Prometheus] (scrape)
           └─► [ELK] (log ingestion)
```

### 7.2. Kubernetes Manifest (simplified)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swift-route-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: swift-route-api
  template:
    metadata:
      labels:
        app: swift-route-api
    spec:
      containers:
      - name: api
        image: ghcr.io/axentx/swift-route-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: swift-route-secrets
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "1"
            memory: "2Gi"
```

### 7.3. CI/CD Pipeline

1. **Lint** – `ruff` for Python, `cargo clippy` for Rust.  
2. **Unit Tests** – `pytest` + `cargo test`.  
3. **Integration Tests** – Spin up Docker Compose with Postgres, Redis, vLLM.  
4. **Build** – Docker images for API, Engine, AI.  
5. **Push** – To GitHub Container Registry.  
6. **Deploy** – Helm chart to AKS / EKS.

### 7.4. Scaling Strategy

- **Stateless API** – Horizontal pod autoscaler on CPU/latency.  
- **AI Selector** – GPU‑enabled nodes; autoscale based on request queue length.  
- **Engine** – Stateless; scale with message queue depth.  
- **Cache** – Redis Cluster with read replicas.  
- **Database** – Primary + read replicas; use logical replication for analytics.

---

## 8. Security & Compliance

- **Authentication** – OAuth2 JWT for API clients.  
- **Encryption** – TLS 1.3 for all external traffic; AES‑256‑GCM for DB at rest.  
- **Audit** – Every transaction event logged to `audit_log`.  
- **Regulatory** – Supports PSD2, AML/KYC hooks (pluggable).  
- **Secrets** – Stored in Vault; rotated nightly.

---

## 9. Monitoring & Alerting

| Metric | Threshold | Alert |
|--------|-----------|-------|
| `api_latency_ms` | > 200ms | `High API latency` |
| `transaction_fail_rate` | > 1% | `Transaction failures` |
| `ai_selector_queue_len` | > 1000 | `AI selector backlog` |
| `db_connection_errors` | > 5/min | `DB connectivity` |

All metrics exposed via `/metrics` endpoint; Grafana dashboards auto‑generated.

---

## 10. Future Enhancements

1. **Multi‑AI Models** – Switch between LLMs based on cost/latency.  
2. **Dynamic FX Rates** – Integrate real‑time market feeds.  
3. **GraphQL API** – For flexible client queries.  
4. **Serverless Functions** – For low‑volume edge cases.  

---

*Prepared by: Senior Product/Engineering Lead – Axentx*
