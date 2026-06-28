## partner-targets.md  
**Product:** **swift‑route** – AI‑driven low‑latency payment routing for cross‑border & digital‑asset flows  
**Goal:** Build a “plug‑and‑play” ecosystem that lets banks, PSPs, and crypto‑exchanges route payments through the optimal network (SWIFT, SEPA, ACH, Ripple, Stellar, etc.) while capturing revenue via affiliate or revenue‑share agreements.

---  

### 1. Integration Roadmap (Quarter‑by‑Quarter)

| Quarter | Milestone | Partner(s) | Integration Type | Expected Impact (Revenue‑share / New Users) |
|---------|-----------|------------|------------------|---------------------------------------------|
| **Q1‑24** | Core routing engine + AI model exposure via REST + webhook callbacks | **1. Stripe Connect** (Payments API) | **S** – OAuth + simple webhook | 5‑10% of Stripe‑Connect onboarding fees (≈ $0.30 / txn) |
| **Q1‑24** | Compliance & KYC data enrichment | **2. Trulioo GlobalGateway** | **M** – API key + batch verification | 2‑3% of verified‑user fees (≈ $0.10 / KYC) |
| **Q2‑24** | Real‑time FX rates & hedging | **3. Open Exchange Rates** (free tier 1,000 req/day) | **S** – GET endpoint, cache layer | 1‑2% of FX‑spread capture (≈ $0.05 / FX conversion) |
| **Q2‑24** | Crypto‑asset settlement bridge | **4. Circle API** (USDC on‑ramp) | **M** – OAuth + webhook for settlement status | 3‑5% of Circle on‑ramp volume (≈ $0.20 / USDC txn) |
| **Q3‑24** | Bank‑to‑bank connectivity (SWIFT & SEPA) | **5. Currencycloud** (global payments) | **L** – SFTP + API + compliance workflow | 4‑6% of cross‑border volume (≈ $0.40 / txn) |
| **Q3‑24** | AML transaction monitoring | **6. Sift Science** (risk scoring) | **M** – SDK + webhook | 1‑2% reduction in fraud loss → indirect revenue uplift |
| **Q4‑24** | Treasury & liquidity management | **7. Kyriba** (cash‑management SaaS) | **L** – SOAP + REST + OAuth | 2‑3% of treasury‑module subscription fees (≈ $0.15 / corp) |
| **Q4‑24** | Enterprise ERP invoicing sync | **8. NetSuite (Oracle)** | **M** – SuiteTalk REST + webhook | 1‑2% of ERP‑linked transaction volume (≈ $0.08 / invoice) |

> **Key:**  
> *S = Small effort (≤ 2 weeks, < 2 dev‑days).  
> *M = Medium effort (2‑4 weeks, 3‑5 dev‑days).  
> *L = Large effort (≥ 4 weeks, > 5 dev‑days, possible security audit).  

---

### 2. Detailed Partner List  

| # | Partner / API | Free‑Tier / Limits | Integration Effort | Primary User Job Solved | Revenue‑Share / Affiliate Model |
|---|---------------|-------------------|--------------------|--------------------------|---------------------------------|
| **1** | **Stripe Connect** – Payments & payouts API | $0, up to 100 test accounts, 10 k API calls/mo | **S** – OAuth flow + `payment_intent` webhook | *Instantly accept & forward payments* across regions | 5 % of Stripe Connect onboarding fee (per linked account) |
| **2** | **Trulioo GlobalGateway** – Global KYC/AML verification | 1 k free verifications/mo | **M** – Batch request + webhook for status | *Verify counterparties* before routing | $0.10 per successful verification (affiliate) |
| **3** | **Open Exchange Rates** – Real‑time FX rates | 1 k requests/day, 1 % historical data | **S** – Simple GET, cache 5‑min | *Select cheapest currency path* (AI uses live rates) | Fixed $0.05 per FX conversion (revenue‑share) |
| **4** | **Circle API** – USDC on‑ramp & off‑ramp | $0, up to $10 k volume/mo | **M** – OAuth, webhook for settlement | *Bridge fiat ↔ digital assets* for crypto‑exchanges | 3 % of Circle transaction fee (paid to Axentx) |
| **5** | **Currencycloud** – Global bank transfers (SWIFT, SEPA, ACH) | $0, 5 k test transfers/mo | **L** – SFTP + API, compliance workflow | *Route payments through optimal banking corridor* | 4 % of gross margin on each cross‑border transfer |
| **6** | **Sift Science** – Fraud & AML scoring | 5 k events/mo | **M** – SDK + webhook for risk verdicts | *Prevent routing of high‑risk transactions* | 1 % of prevented fraud loss (shared savings) |
| **7** | **Kyriba** – Treasury & liquidity SaaS | 30‑day trial, 1 k API calls | **L** – SOAP + REST, OAuth2 | *Optimize cash positioning & netting* before routing | 2 % of Kyriba subscription revenue per linked client |
| **8** | **NetSuite (Oracle)** – ERP invoicing & AP/AR | 1000 API calls/mo (sandbox) | **M** – SuiteTalk REST + webhook | *Auto‑reconcile routed payments with invoices* | 1 % of NetSuite transaction volume (per invoice) |

---

### 3. Prioritisation Criteria  

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Revenue‑share potential** | 30 % | Direct cash flow; partners with per‑txn splits are top priority |
| **Market reach / install base** | 25 % | Larger partner ecosystems accelerate user acquisition |
| **Integration complexity** | 20 % | Faster wins (S/M) allow early proof‑of‑concept and cash flow |
| **Strategic fit to core value (AI routing)** | 15 % | Must provide data or network that improves path‑selection |
| **Compliance / KYC coverage** | 10 % | Reduces regulatory risk for banks & crypto firms |

Applying the weighted score yields the ordering shown in the roadmap (Stripe → Trulioo → Open Exchange → Circle → Currencycloud → Sift → Kyriba → NetSuite).

---

### 4. Affiliate / Revenue‑Share Negotiation Tips  

1. **Bundle “AI‑Routing Premium”** – Offer partners a co‑branded UI that showcases the AI‑selected path; negotiate a higher split (e.g., 7 % vs 5 % for Stripe).  
2. **Volume‑based tiered rebates** – For Currencycloud, propose 4 % up to $1 M/mo, 5 % beyond $1 M/mo to incentivise high‑volume banks.  
3. **Joint go‑to‑market** – Pair with Circle on a “Crypto‑to‑Fiat Fast‑Lane” webinar series; share leads and split the first‑month fees 50/50.  
4. **Data‑exchange credits** – Offer partners free access to our anonymised routing performance dataset in exchange for lower API pricing (e.g., Trulioo free tier upgrade).  

---

### 5. Success Metrics (to be tracked per partner)

| Metric | Target (12 mo) |
|--------|----------------|
| **Integrated partners** | ≥ 6 (≥ 4 revenue‑share) |
| **Total routed volume** | $250 M |
| **Average latency reduction** | 30 % vs baseline |
| **Revenue from affiliate splits** | $1.2 M |
| **New paying customers acquired via partner referrals** | 150 + |

---  

*Prepared by Business‑Synthesis – Axentx OS*  