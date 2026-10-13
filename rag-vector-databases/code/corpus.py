"""The invented help centre used by every example in this module.

Fernpay is a made-up invoicing product. Each document has metadata: a status (current or
retracted), an audience (customer or internal) and a date. The eval set lists real-looking
questions and the chunk that answers each one. Nothing here describes a real company.
"""

DOCS = [
    dict(id="refunds-v2", title="Refund policy", status="current", audience="customer", updated="2026-03", text="""
## Annual plans
Annual plans can be refunded within 14 days of purchase. Ask from Settings > Billing.
## Monthly plans
Monthly plans are not refunded. You can cancel at any time and keep access until the end of the billing period.
"""),
    dict(id="refunds-v1", title="Refund policy (old)", status="retracted", audience="customer", updated="2025-01", text="""
## Annual plans
Annual plans can be refunded within 30 days of purchase. Ask from Settings > Billing.
## Monthly plans
Monthly plans can be refunded within 7 days of the latest charge.
"""),
    dict(id="cancel", title="Ending your subscription", status="current", audience="customer", updated="2026-02", text="""
## How to end your plan
Go to Settings > Billing and choose End plan. Billing stops at the end of the current period.
## What happens to your data
Your workspace stays readable for 90 days after the plan ends. Export it before then.
"""),
    dict(id="errors", title="Bank feed error codes", status="current", audience="customer", updated="2026-01", text="""
## E-4021
Error E-4021 means the bank feed timed out. Reconnect the bank in Settings > Connections.
## E-4022
Error E-4022 means the bank rejected the saved login. Enter the bank password again in Settings > Connections.
## E-4030
Error E-4030 means the bank does not support automatic feeds. Upload a statement file instead.
"""),
    dict(id="invoices", title="Working with invoices", status="current", audience="customer", updated="2026-02", text="""
## Create an invoice
Choose New invoice, add line items and a client, then press Send.
## Recurring invoices
A recurring invoice is sent to the client on a schedule, for example on the first day of every month.
## Late payment reminders
Fernpay can email a reminder when an invoice is overdue. Turn on reminders per client.
"""),
    dict(id="data", title="Your data", status="current", audience="customer", updated="2026-01", text="""
## Export
Export all invoices, clients and payments as a CSV file from Settings > Export.
## Data residency
Workspaces created in the EU region are stored in Frankfurt. Other workspaces are stored in Virginia.
"""),
    dict(id="api", title="API limits", status="current", audience="customer", updated="2026-04", text="""
## Rate limit
The API accepts 600 requests per minute for each workspace. Extra requests get error 429.
## Keys
Create an API key in Settings > Developers. A key belongs to one workspace.
"""),
    dict(id="pricing", title="Plans and prices", status="current", audience="customer", updated="2026-03", text="""
## Plans
Starter costs 12 dollars a month. Team costs 39 dollars a month for up to 10 users.
## Annual billing
Annual billing costs the same as 10 months.
"""),
    dict(id="tax", title="Tax on invoices", status="current", audience="customer", updated="2025-11", text="""
## VAT in the EU
For a business client in another EU country, Fernpay adds a reverse charge note and no VAT.
## Sales tax in the US
Fernpay does not file sales tax. Add the rate for each state yourself.
"""),
    dict(id="runbook", title="Support runbook", status="current", audience="internal", updated="2026-04", text="""
## Large refunds
A refund over 5,000 dollars needs approval from finance before support confirms it.
## Goodwill credits
Support can give a credit of up to one month without approval.
"""),
]

# Each question names the chunk that answers it and the fact that answer must contain.
# "kind" says what the question tests.
EVAL = [
    dict(q="how do I stop paying for fernpay", fact="choose End plan", gold="cancel#0", kind="paraphrase"),
    dict(q="can I get my money back on a yearly plan", fact="within 14 days", gold="refunds-v2#0", kind="paraphrase"),
    dict(q="bank connection keeps timing out", fact="bank feed timed out", gold="errors#0", kind="paraphrase"),
    dict(q="automatically nudge clients who have not paid yet", fact="email a reminder", gold="invoices#2", kind="paraphrase"),
    dict(q="where is my data kept if I am in Germany", fact="stored in Frankfurt", gold="data#1", kind="paraphrase"),
    dict(q="bill a client every month without doing it by hand", fact="first day of every month", gold="invoices#1", kind="paraphrase"),
    dict(q="download everything as a spreadsheet", fact="as a CSV file", gold="data#0", kind="paraphrase"),
    dict(q="how many calls per minute can the API take", fact="600 requests per minute", gold="api#0", kind="mixed"),
    dict(q="what does E-4021 mean", fact="bank feed timed out", gold="errors#0", kind="exact"),
    dict(q="E-4022", fact="rejected the saved login", gold="errors#1", kind="exact"),
    dict(q="fix E-4030", fact="Upload a statement file", gold="errors#2", kind="exact"),
    dict(q="error 429", fact="get error 429", gold="api#0", kind="exact"),
]
