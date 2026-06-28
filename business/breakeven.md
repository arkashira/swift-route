# breakeven.md  

**Product:** swift‑route – AI‑driven low‑latency payment routing platform  
**Target customers:** banks, payment service providers, corporate treasury groups, digital‑asset exchanges  

---  

## 1. Unit Economics (per active user / month)

| Cost Component | Assumptions | Monthly Cost (USD) |
|----------------|-------------|--------------------|
| **Compute** (GPU‑accelerated inference + routing engine) | 2 vCPU + 8 GB RAM + 1 x NVIDIA T4 (0.5 h inference per 1 k tx) → 0.02 GPU‑hour per active user, $0.90 per GPU‑hour (spot) | **$0.02** |
| **Storage** (transaction logs, audit trail, model snapshots) | 5 GB per active user @ $0.02/GB (cold‑storage tier) | **$0.10** |
| **Bandwidth** (bi‑directional data transfer) | 2 GB outbound + 0.5 GB inbound per user @ $0.09/GB (cloud egress) | **$0.23** |
| **Third‑party APIs** (FX rates, KYC checks) | 100 API calls @ $0.001 each | **$0.10** |
| **Support / Ops overhead** (monitoring, alerts) | Pro‑rated share of $5 k monthly ops budget across 5 000 target users | **$1.00** |
| **Total Variable Cost / Active User / Mo** |  | **$1.45** |

> **Note:** Fixed overhead (R&D, security audits, compliance, office) is treated separately in the break‑even model.

---

## 2. Pricing Tiers  

| Tier | Monthly Price (USD) | Features | Expected Gross Margin* |
|------|--------------------|----------|------------------------|
| **Starter** | **$9** | • Up to 5 k routed transactions / mo  <br>• Basic AI path selection (single model) <br>• Email support <br>• SLA 99.5% | 84% |
| **Professional** | **$49** | • Up to 50 k transactions / mo  <br>• Multi‑model AI selection (FX, crypto, legacy) <br>• Real‑time dashboard & alerts <br>• Phone/email support <br>• SLA 99.9% | 97% |
| **Enterprise** | **$199** | • Unlimited transactions <br>• Custom model training & on‑prem deployment option <br>• Dedicated account manager <br>• 24/7 premium support, SLA 99.99% <br>• Compliance & audit reporting | 99% |

\*Margin = (Price – Variable Cost per active user) / Price.  
Variable cost per active user is $1.45 (see above). For Enterprise we assume a higher‑value user consumes ~10× the compute/storage, raising variable cost to $14.5; margin still ~92% but the higher price drives overall profitability.

---

## 3. Customer Acquisition Cost (CAC)

| Source | Cost per Lead | Conversion Rate (Lead → Paid) | CAC (USD) |
|--------|---------------|------------------------------|-----------|
| Paid digital (LinkedIn, industry sites) | $120 | 5 % | **$2,400** |
| Channel / partner referrals | $80 | 8 % | **$1,000** |
| Direct sales (field reps) | $250 | 10 % | **$2,500** |

**CAC range:** **$1 k – $2.5 k** per new paying customer (average ≈ $1,800).  

Assume a blended acquisition mix of 40 % paid digital, 30 % partner, 30 % direct → **average CAC ≈ $1,800**.

---

## 4. Lifetime Value (LTV)

*Assumptions*  

| Parameter | Value |
|-----------|-------|
| Average monthly revenue per user (ARPU) | $49 (Professional tier) |
| Gross margin (average) | 95 % |
| Churn rate | 5 % per month (high‑touch B2B SaaS) |
| Customer lifetime (months) | 1 / churn = 20 mo |
| Discount rate (monthly) | 0.8 % (≈10 % annual) |

**LTV calculation (simplified):**  

\[
LTV = \sum_{t=1}^{20} \frac{ARPU \times Margin}{(1+0.008)^t}
\approx \frac{49 \times 0.95}{0.008} \times (1 - (1+0.008)^{-20}) \approx \$830
\]

Rounded **LTV ≈ $830** per customer.

*Payback period* = CAC / (ARPU × Margin) = $1,800 / ($49 × 0.95) ≈ **38 months** – acceptable for high‑value enterprise contracts when bundled with multi‑year deals (typical 2‑yr contracts → upfront cash improves payback).

---

## 5. Break‑Even Users Count  

**Fixed monthly overhead** (post‑launch, includes:  

* Engineering & DevSecOps salaries (3 FTE) – $30 k  
* Compliance & audit – $5 k  
* Marketing & sales ops – $10 k  
* Cloud reserved instances (baseline) – $8 k  

**Total Fixed OPEX:** **$53,000 / month**

**Contribution margin per user** (average across tiers, weighted 20 % Starter, 60 % Professional, 20 % Enterprise):

| Tier | % Users | Price | Variable Cost | Contribution |
|------|---------|-------|---------------|--------------|
| Starter | 20 % | $9 | $1.45 | $7.55 |
| Professional | 60 % | $49 | $1.45 | $47.55 |
| Enterprise | 20 % | $199 | $14.5* | $184.5 |

Weighted average contribution ≈ **$38.5 per user / month**.

**Break‑even user count** = Fixed OPEX / Avg. contribution  

\[
\frac{53,000}{38.5} \approx **1,378 \text{ active paying users}**
\]

Rounded **≈ 1.4 k users** to cover all monthly costs.

---

## 6. Path to $10 k MRR  

| Target MRR | Tier Mix (users) | Calculation |
|------------|------------------|-------------|
| $10,000 | 5 × Enterprise + 30 × Professional + 20 × Starter | (5 × $199) + (30 × $49) + (20 × $9) = $995 + $1,470 + $180 = **$2,645** – not enough |
| Adjusted mix | 10 × Enterprise + 60 × Professional + 40 × Starter | (10 × 199) + (60 × 49) + (40 × 9) = $1,990 + $2,940 + $360 = **$5,290** |
| Final mix to hit $10 k | 20 × Enterprise + 120 × Professional + 80 × Starter | (20 × 199) + (120 × 49) + (80 × 9) = $3,980 + $5,880 + $720 = **$10,580** |

**Result:** **~220 paying customers** (20 Enterprise, 120 Professional, 80 Starter) yields **≈ $10.6 k MRR**.  

*Alternative faster route:* Secure a single 2‑year Enterprise contract at **$199 × 12 × 2 = $4,776** upfront → counts as ~2 k MRR (annualized), reducing the number of smaller accounts needed.

---

### Quick Takeaways  

* **Unit cost** is low ($1.45/user) thanks to spot GPU and cold storage.  
* **Pricing** provides >80 % gross margin even at the low tier.  
* **CAC** (~$1.8 k) is higher than LTV ($830) for a single‑month churn scenario, so we must **drive longer contracts** (≥12 mo) and/or **increase ARPU** (e.g., add value‑added modules).  
* **Break‑even** at ~1.4 k paying users; with a realistic acquisition plan of 30 % Enterprise, 60 % Professional, 10 % Starter, this translates to roughly **2 k total accounts** after ~6 months of ramp‑up.  
* **$10 k MRR** is reachable with a modest mix of 20 Enterprise + 120 Professional + 80 Starter accounts, or by landing a few multi‑year Enterprise deals.  

These numbers form the financial backbone for the go‑to‑market plan and will be refined as real usage and churn data arrive.  