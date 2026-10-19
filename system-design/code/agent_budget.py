"""An agent platform loop: a permissioned tool gateway, step and cost budgets, a kill switch, and checkpoints so a crash resumes
instead of repeating paid or irreversible tool calls. Run: python3 agent_budget.py"""


class Gateway:
    def __init__(self, allowed, cost):
        self.allowed, self.cost, self.calls = set(allowed), cost, []

    def call(self, tool):
        if tool not in self.allowed:
            return "denied"
        self.calls.append(tool)
        return "ok"


def run_agent(plan, gateway, max_steps, max_cost, checkpoint, crash_at=None, killed=lambda: False):
    """plan: tools the model asks for, in order. checkpoint: dict holding the number of completed steps."""
    spent = sum(gateway.cost.get(t, 0) for t in gateway.calls)
    while checkpoint["done"] < len(plan):
        if killed():
            return "killed"
        if checkpoint["done"] >= max_steps:
            return "step budget"
        tool = plan[checkpoint["done"]]
        if spent + gateway.cost.get(tool, 0) > max_cost:
            return "cost budget"
        if gateway.call(tool) == "ok":
            spent += gateway.cost.get(tool, 0)
        checkpoint["done"] += 1                                  # committed after the call, as in a workflow engine
        if crash_at == checkpoint["done"]:
            return "crashed"
    return "finished"


if __name__ == "__main__":
    cost = {"search": 1, "send_email": 5, "charge_card": 20}
    plan = ["search", "search", "send_email", "charge_card", "search"]
    g = Gateway(["search", "send_email", "charge_card"], cost)
    cp = {"done": 0}
    first = run_agent(plan, g, 10, 100, cp, crash_at=3)
    resumed = run_agent(plan, g, 10, 100, cp)                    # restart from the checkpoint
    print(f"first run {first} after {3} steps; resumed run {resumed}; tool calls made {len(g.calls)} (no repeats)")
    g2 = Gateway(["search"], cost)
    denied = g2.call("charge_card")
    g3, cp3 = Gateway(["search", "send_email", "charge_card"], cost), {"done": 0}
    over = run_agent(plan, g3, 10, 10, cp3)
    stop = run_agent(plan, Gateway(["search"], cost), 10, 100, {"done": 0}, killed=lambda: True)
    print(f"unpermitted tool: {denied}; cost budget of 10: {over} after {len(g3.calls)} calls; kill switch: {stop}")
    assert first == "crashed" and resumed == "finished" and len(g.calls) == 5
    assert denied == "denied" and over == "cost budget" and len(g3.calls) == 3 and stop == "killed"
    print("agent budget ok")
