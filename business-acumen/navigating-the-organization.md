# Navigating the organization: how the company really works

*Part of [Business acumen for the product leader](./README.md)*

*Last reviewed: 2026-10 · Volatility: medium*

## TL;DR

Every company has two maps. The **formal organization** is the org chart: who reports to whom, who owns which budget. The **informal organization** is the network of trust, favours and information that decides what actually happens. A product leader needs both maps, and one more: a clear view of how the company makes money.

The core tradeoff is time and credibility. Building relationships, sponsors and political capital takes months. Skipping that work feels faster, until a decision you need is made in a room you were not in. At Group PM level and above, most of your outcomes depend on people who do not report to you.

> 🎯 **For the product leader**
>
> **Why it matters** — Your biggest decisions need yes from Finance, Risk, Sales, Operations and sometimes an outside partner. Each of them is measured on something different. If you do not know what they are paid to protect, you cannot design a proposal they can accept.
>
> **What it changes in your decisions** — You map who decides and what they fear before you write the proposal. You spend political capital on purpose, on the few fights that matter.
>
> **Ask your team** — *"Who outside this room can stop this, and have we talked to them yet?"*
>
> **Risk if ignored** — A well-built launch is blocked a week before release by a compliance review, a partner bank or a finance sign-off that nobody on the team knew existed.

## Mental model: the road map and the traffic

```mermaid
flowchart LR
  subgraph FORMAL["FORMAL: the org chart"]
    CEO["CEO"] --> CFO["Finance"]
    CEO --> CRO["Risk and Compliance"]
    CEO --> CPO["Product"]
    CEO --> CRO2["Sales and Ops"]
  end
  subgraph INFORMAL["INFORMAL: trust and information"]
    P["You"] -.->|"trusted peer"| F2["Finance partner"]
    P -.->|"asks for advice"| M["Mentor"]
    S["Sponsor"] -.->|"speaks for you"| CEO
    F2 -.->|"early warning"| P
  end
```

The org chart is the road map. It shows the official routes. The informal network is the traffic. It shows which routes are open today, and which shortcut a trusted peer can give you.

**Where the analogy breaks.** Roads do not remember you. People do. Every interaction changes the informal map. A shortcut you abuse closes for good.

## How the company actually makes money

Start with the money engine. Write it in two sentences. Then check it with a finance partner. Most leaders get one part wrong.

Every business has a revenue engine, a cost base, and one or two constraints that limit growth. The table shows how this differs by domain, using public company disclosures.

| Domain | How revenue is earned | What limits growth | A public example |
| --- | --- | --- | --- |
| **Payments** | A fee on each payment processed | Fraud, disputes and the fees paid to card networks and issuers | Adyen prices many card payments as **interchange++**: the card's interchange fee, plus network fees, plus Adyen's own fee. Its markup is visible apart from the pass-through costs. |
| **Lending** | Interest and fees on loans | Credit losses and the cost of funding the loans | SoFi agreed in 2021 to buy a community bank to accelerate its pursuit of a national bank charter. The aim was to fund loans with deposits, a cheaper source than the market funding a non-bank relies on. |
| **eCommerce** | A share of each order, plus ads and subscriptions | Delivery cost, and the supply of merchants and couriers | Instacart reports two revenue lines: transaction revenue and advertising and other revenue. Brands pay to reach shoppers. |
| **InsurTech** | Premium, minus claims and expenses | Loss ratio, capital and reinsurance | Lemonade's 2020 filings described keeping a fixed share of premium as its fee. The rest paid claims and reinsurance. It aimed to give any leftover money to charities its customers chose. |
| **Retail** | Product margin on goods sold | Inventory, store costs and markdowns | Walmart's comparable-sales figure includes eCommerce sales, not only sales in its stores. In general, a shared metric like this can help align store and online teams. |
| **FinTech** | Fees, interchange and interest on balances | Regulation, partner banks and cost to serve | Nubank reports its monthly cost to serve each active customer. In 2023 it said that cost stayed below one US dollar. |

Once you know the engine, you know which functions hold the levers. In a lender, Credit Risk owns the approval cutoff. In a payments company, the Risk team owns fraud rules. In a retailer, Merchandising owns the range and the stock budget.

## The formal organization: where decisions are made

The formal org decides money and headcount through a few fixed processes. Learn their calendar.

- **The annual plan.** Finance sets revenue and cost targets for each unit. Headcount is fixed here. A bet not in the plan needs a trade-off later.
- **Quarterly reviews.** Leaders report against plan. Shortfalls trigger cuts or shifts.
- **Investment or portfolio committees.** Large bets are approved here. See [lesson 9](./portfolio-strategy-and-allocation.md).
- **Risk and compliance sign-offs.** In regulated domains, a product cannot launch without them. These often sit outside the product calendar.
- **Partner approvals.** A fintech that uses a partner bank needs that bank's approval for new products. An insurance agency needs the carrier that holds the risk. These approvers are not on your org chart at all.

## The informal organization: trust, capital and sponsors

**Political capital** is the stock of trust you can draw on to get things done. Think of it as an account.

| Deposits | Withdrawals |
| --- | --- |
| Delivering what you promised | Escalating a peer to their boss |
| Giving credit to other teams in public | Asking for an exception to a process |
| Sharing information early | Surprising a peer in a large meeting |
| Helping a peer hit their target | Missing a commitment you made to them |
| Keeping a confidence | Reversing a decision they relied on |

Withdrawals are not bad. They are the point of saving. Spend capital on the two or three decisions that change your year. Do not spend it on a slide format or a meeting time.

**Mentors and sponsors are different.** A **mentor** gives you advice. A **sponsor** spends their own capital to argue for you in rooms you are not in, such as promotion or staffing discussions. You earn a sponsor by making them look right for backing you. Most leaders have mentors. Fewer have a sponsor. At VP level, a sponsor often decides whether you get the next scope.

## Managing conflict

Conflict between functions is normal. Each function is paid to protect something. The design question is how to make the conflict useful.

1. **Separate positions from interests.** Risk says "no launch." Its interest is "no unexpected losses." A launch with a loss cap may meet that interest.
2. **Agree on the facts first.** Write the shared facts in one document. Most fights are about different numbers.
3. **Name the decision owner.** If nobody owns the call, the loudest voice wins. See [lesson 3](./teams-and-collaboration.md).
4. **Escalate together.** If you cannot agree, write one page with both views and take it up together. A joint escalation costs little capital. A solo escalation costs a lot.

## Influence across functions

To influence a function, know what it is measured on and what it fears.

| Function | Measured on | Fears | What helps them say yes |
| --- | --- | --- | --- |
| Finance | Plan accuracy, margin, cash | Surprises and unfunded costs | A business case with a sensitivity table |
| Risk and Compliance | Losses, regulatory findings | An issue a regulator finds first | Early involvement and a loss cap |
| Sales | Bookings against quota | Losing deals to a missing feature | A date they can tell customers |
| Operations | Cost per case, service levels | Volume spikes with no staff | A volume forecast and a runbook |
| Engineering | Delivery, reliability | Rushed scope and on-call pain | Clear scope and time for quality |

## Worked example: launching instant payouts at a payments company

*This example is invented, to show the method. The company and numbers are illustrative.*

A payments company pays merchants their sales in two business days. The VP of Product wants to offer instant payouts for a fee. She assumes a fee of 1% of each payout.

**Step 1: map the money.** Assume merchants would move $50 million a month through instant payouts. At 1%, that is $500,000 a month in fee revenue.

**Step 2: map who decides, and what they fear.**

| Stakeholder | What they fear | What they need |
| --- | --- | --- |
| Treasury | Paying merchants before the card networks settle with the company. That needs cash on hand. | A funding estimate. At two days of early payout on $50 million a month, the company pre-funds about $3.3 million at any time ($50 million ÷ 30 days × 2 days). |
| Risk | A fraudster takes sales, cashes out instantly, and the disputes arrive weeks later. | Eligibility rules, such as a minimum account age, and a daily cap per merchant. |
| Finance | Fee revenue counted before losses | A net figure after expected losses and funding cost |
| Operations | Support tickets about failed payouts | A help article and a status page |

**Step 3: adjust the proposal to their interests.** The VP adds eligibility rules and a daily cap. She asks Finance to model the funding cost. Assume 5% a year on $3.3 million. That is about $165,000 a year, or about $14,000 a month.

**Step 4: spend capital on one point only.** Risk wants a 90-day account age. The VP agrees, except for merchants with a clean dispute history. That is the one point she argues.

**Step 5: pre-wire.** She meets each stakeholder alone before the decision meeting. The meeting confirms what was already agreed.

The result: about $486,000 a month net of funding cost, before losses. Risk's eligibility rules keep loss exposure inside a cap that Risk set itself.

## Tradeoffs and decisions

- **Speed vs. support.** Pre-wiring every stakeholder takes days. Skipping it saves days and risks a late veto.
- **Visibility vs. trust.** Credit given to other teams builds trust. It costs you some visibility with your own leadership.
- **Fight now vs. save capital.** Every fight you win costs capital. Pick the fights that change the outcome.
- **Formal vs. informal routes.** Informal routes are fast. They leave no record, so a decision made in a hallway can be undone in a review.

## Failure modes

- **The invisible approver.** A partner bank, a carrier or a regulator-facing team blocks a launch late. Nobody mapped them.
- **Capital spent on small things.** The leader argues every point and has nothing left for the one that matters.
- **Sponsor without delivery.** A sponsor backs you once. You miss, and they stop.
- **Conflict without an owner.** Two functions argue for weeks because nobody holds the decision.
- **The org chart illusion.** The leader assumes the boss of a function makes its decisions. A trusted senior expert often does.

## Under the hood

A stakeholder map works best as a shared, plain file. Keep it next to the proposal.

```yaml
initiative: instant-payouts
decision_owner: VP Product
decision_date: 2026-11-15
stakeholders:
  - function: Treasury
    person_role: Head of Treasury
    measured_on: [liquidity buffer, funding cost]
    interest: "never pre-fund beyond the approved limit"
    position_today: neutral
    pre_wire: done
  - function: Risk
    person_role: Head of Merchant Risk
    measured_on: [loss rate, dispute rate]
    interest: "no loss above the agreed cap"
    position_today: against
    ask: "eligibility rules plus a daily cap"
    pre_wire: scheduled
  - function: Partner bank
    person_role: Partner compliance lead
    approval_required: true
    lead_time_days: 30
```

## Practitioner checklist

- [ ] Write two sentences on how the company makes money. Get a finance partner to correct them.
- [ ] List every approval a launch in your area needs, including outside partners.
- [ ] For your next big decision, list each stakeholder's measure, fear and need.
- [ ] Name the decision owner for each open cross-team conflict.
- [ ] Pre-wire every key stakeholder alone before the decision meeting.
- [ ] Name your sponsor. If you cannot, decide whose sponsor you want to earn.
- [ ] Count your political capital spends this quarter. Cut the ones on small points.

## Related lessons

- [Teams and collaboration](./teams-and-collaboration.md) — decision rights that stop conflicts without owners.
- [Executive influence and stakeholders](./executive-influence-and-stakeholders.md) — the executive table and negotiation.
- [Communication](../product-sense/communication.md) — influencing stakeholders with artifacts and story.
- [Working with engineering](../technical-product-management/working-with-engineering.md) — the closest partnership a product leader has.
- [Transactional and financial systems](../system-design/transactional-and-financial.md) — how payment systems settle and pay out.

## Sources and notes

- The instant payouts example, its numbers and the stakeholder map are invented and illustrative. The 1% fee and 5% funding rate are assumed.
- Adyen, help article *What is the interchange ++?*: the card's interchange, plus scheme fees, plus Adyen's own fee. [Adyen](https://help.adyen.com/knowledge/payment-methods/explore-payment-methods/what-is-the-interchange). As of 2026-10.
- SoFi, press release of 2021-03-09 announcing the agreement to acquire Golden Pacific Bancorp, a community bank: to accelerate its pursuit of a national bank charter, and to lower its cost of funding versus a non-bank. [SoFi](https://www.sofi.com/newsroom/sofi-announces-agreement-acquire-golden-pacific-bancorp-inc/). As of 2026-10.
- Maplebear (Instacart), Form 10-K for fiscal 2025 (filed 2026-02): revenue consists of transaction revenue and advertising and other revenue. [Form 10-K](https://www.sec.gov/Archives/edgar/data/1579091/000157909126000018/cart-20251231.htm). As of 2026-10.
- Lemonade, Form 10-K for fiscal 2020 (filed 2021-03): fixed-fee model and Giveback. [Form 10-K](https://www.sec.gov/Archives/edgar/data/1691421/000169142121000024/lmda-20201231.htm). As of 2026-10.
- Walmart, Form 10-K for fiscal 2026 (year ended 2026-01-31, filed 2026-03): comparable sales include eCommerce sales, measured as all sales initiated digitally. [Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm). As of 2026-10.
- Nu Holdings, second quarter 2023 results (2023-08-15): monthly cost to serve per active customer of $0.8, below one US dollar. [Nu newsroom](https://nu.com/en/newsroom/company/nu-holdings-ltd-reports-second-quarter-2023-financial-results). As of 2026-10.
