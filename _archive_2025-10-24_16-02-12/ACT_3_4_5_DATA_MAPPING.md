# Act 3-5 Data Mapping (Anti-Hallucination)

**Purpose**: Map real JSON data to Acts 3-5 to eliminate hallucinations

**Date**: 2025-10-23

---

## Available Real Data Sources

| File | Size | Records | Use For |
|------|------|---------|---------|
| `customer-insights.json` | 11K | 261+ reviews analyzed | Act 3 - Customer insights |
| `customer-segments.json` | 12K | 5 segments | Act 3 - Customer deep dive |
| `corporate-clients.json` | 21K | 52 Fortune 500 companies | Act 4 - Market proof |
| `use-cases.json` | 14K | 35+ use cases | Act 3 - Real use cases |
| `origin-stories.json` | 17K | Sourcing stories | Act 4 - Supply chain proof |
| `certifications.json` | 14K | Quality certifications | Act 4 - Quality proof |
| `claims-registry.json` | 21K | FSSAI nutritional claims | Act 4 - Nutritional proof |
| `founder-story.json` | 18K | Brand journey | Act 5 - Vision context |
| `README.json` | 6K | Overview | All acts - Context |

**Total Real Data**: 9 JSON files, ~140KB structured data

---

## Act 3: What We Discovered

### Document Structure (Data-Driven)

**Document 00: Research Methodology**
- Data Sources: List actual JSON files used
- Review Count: 261+ (from customer-insights.json)
- Platforms: Amazon, Flipkart, BigBasket, Google Reviews, Instagram, Reddit
- **❌ REMOVE**: "25 interviews", "500+ support tickets" (hallucinated)

**Document 01: Customer Deep Dive**
- Source: `customer-segments.json`
- 5 Real Segments:
  1. Premium Health Seekers (35% revenue)
  2. Global Indians (25% revenue)
  3. Luxury Conscious (15% revenue)
  4. Affluent Parents (15% revenue)
  5. Corporate Gifters (10% revenue)
- Real demographics, psychographics, purchase behavior for each

**Document 02: Pain Points & Desires**
- Source: `customer-insights.json` → painPoints array
- 15 real pain points with customer quotes
- Severity ratings, frequency data
- **❌ REMOVE**: All fabricated pain points not in JSON

**Document 03: Use Cases & Moments**
- Source: `use-cases.json`
- 35+ real use cases across products
- "Who Chooses + The Moment + Why It Works" structure
- Real customer quotes

**Document 04: Key Insights Summary**
- Synthesize from real data only
- No fabricated market sizes
- No invented competitive gaps

---

## Act 4: Market Proof

### Document Structure (Data-Driven)

**Document 00: Corporate Validation**
- Source: `corporate-clients.json`
- 52 Fortune 500 companies (real clients)
- Sectors: Technology, Finance, Consulting, E-commerce, Healthcare, FMCG
- Use Cases: Corporate Gifting, Office Pantries, Employee Wellness
- Repeat rate: 85%
- **Real companies**: Google, Microsoft, Amazon, Goldman Sachs, McKinsey, etc.

**Document 01: Quality Certifications**
- Source: `certifications.json`
- Real certifications (FSSAI, cold chain, etc.)
- Verification methods
- **❌ REMOVE**: Fabricated certifications

**Document 02: Customer Sentiment**
- Source: `customer-insights.json`
- 261+ reviews analyzed
- Sentiment: 68% positive, 18% neutral, 14% negative
- Overall score: 7.2/10
- Real customer quotes

**Document 03: Nutritional Claims**
- Source: `claims-registry.json`
- FSSAI-compliant nutritional claims
- Product-specific benefits
- No fabricated health claims

**Document 04: Supply Chain Proof**
- Source: `origin-stories.json`
- Real sourcing stories
- Verifiable origins

---

## Act 5: Where We Should Go

### Document Structure (Strategic, Not Fabricated)

**Approach**: Use insights from Acts 3-4 to guide strategy, but:
- ❌ NO fabricated revenue projections (₹3-5 Cr, etc.)
- ❌ NO invented market sizes (₹150 Cr, ₹300 Cr, etc.)
- ❌ NO made-up pricing (₹99 single-serve, ₹999 boxes, etc.)
- ✅ YES strategic direction based on real pain points
- ✅ YES recommendations grounded in customer segments
- ✅ YES initiatives aligned with corporate client needs

**Document 00: Strategic North Star**
- Vision based on founder-story.json
- Positioning grounded in real differentiators (cold chain, Fortune 500, etc.)

**Document 01: Priority Initiatives**
- Based on real pain points from customer-insights.json
- Address real customer segment needs from customer-segments.json
- Leverage real corporate relationships from corporate-clients.json

**Document 02: Implementation Roadmap**
- High-level milestones (no fabricated timelines)
- Resource allocation principles (no specific budgets without data)
- Success metrics framework (not fabricated numbers)

---

## Anti-Hallucination Rules for Generators

### ✅ ALLOWED
1. Reading data from JSON files
2. Quoting customer reviews from customer-insights.json
3. Citing Fortune 500 companies from corporate-clients.json
4. Using real segment demographics from customer-segments.json
5. Listing use cases from use-cases.json
6. Formatting/structuring data (markdown, tables)
7. Synthesizing insights (connecting dots between real data)

### ❌ FORBIDDEN
1. Inventing market sizes (₹X Cr market opportunity)
2. Fabricating revenue projections (₹X Cr in Y years)
3. Creating interview counts ("25 interviews")
4. Making up support ticket volumes ("500+ tickets")
5. Inventing competitor valuations ($10M, $27B)
6. Fabricating pricing (₹99, ₹999, ₹5K) not in product JSONs
7. Creating case studies not in corporate-clients.json
8. Making up statistics not in JSON files

---

## Verification Protocol

**Before committing any generator**:
1. Run `python3 verify_hallucinations.py`
2. Ensure 0 hallucinations detected
3. All claims must trace back to JSON source
4. If data missing → add to JSON first, NEVER hard-code

**Enforcement**:
- Pre-commit hook blocks hallucinations
- Tests fail if claims can't be verified
- Manual review required for Acts 3-5

---

## Data Gaps (Need to Fill)

**Missing data that would be useful**:
1. Actual interview transcripts (if 25 interviews happened)
2. Support ticket data (if 500+ tickets exist)
3. Market research reports (if commissioned)
4. Competitor analysis data (if researched)
5. Financial projections model (if created)

**Options**:
- Add real data to JSON files (if available)
- Remove claims entirely (if fabricated)
- Add disclaimer (if illustrative/hypothetical)

---

**Next Steps**:
1. Create `act3_generator.py` using customer-insights.json, customer-segments.json, use-cases.json
2. Create `act4_generator.py` using corporate-clients.json, certifications.json, claims-registry.json
3. Create `act5_generator.py` using strategic framework (no fabrications)
4. Verify 0 hallucinations before committing
