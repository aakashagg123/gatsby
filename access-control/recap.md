# Access control — recap & real-world examples

*Part of [Access control for the technical PM](./README.md)*

## Real-world examples & war stories

**A missing object check tops the API risk list.** The OWASP API Security Top 10 (2023 edition) ranks Broken Object Level Authorization first. That is a ranking of risk, not a count of incidents. It happens when an API accepts an object id, such as an invoice number, and never checks that the caller may access that object. The attacker only changes the id. 🎯 *Takeaway:* a verified login is not a permitted request. Check the object on every endpoint. See the [missing check example](./authentication-authorization-and-the-access-control-model.md). The description comes from search-result summaries of the OWASP entry. The OWASP page could not be opened.

**A misconfiguration, and a regulator's view of cloud access (2019 to 2020).** In 2019 an attacker used a misconfigured web application firewall on Capital One's cloud environment to reach customer data on more than 100 million credit card applicants, according to press and regulator accounts. In August 2020 the US Office of the Comptroller of the Currency assessed an $80 million civil money penalty. It cited weak risk management for the cloud move and gaps in network security controls, data loss prevention, alert handling and audit. 🎯 *Takeaway:* regulators check how you control and monitor access to data in the cloud. Tight configuration, least privilege and monitoring matter as much as the login. This summary comes from search-result excerpts of law-firm and press coverage. The OCC order could not be opened.

**A bug that showed one user another user's data (2023).** On March 20, 2023, a caching bug in a library used by ChatGPT let some users see other users' chat titles. OpenAI said a small share of ChatGPT Plus subscribers could also see some billing details. 🎯 *Takeaway:* leaks need no attacker. Any shared store can cross a boundary. See [memory and context](../memory-and-context/when-memory-goes-wrong.md). Details come from search-result excerpts of press coverage.

**Google built a system for sharing at scale (2019).** Google's Zanzibar paper describes one authorization system serving products such as Calendar, Drive and YouTube, built on stored relationships between users and objects. 🎯 *Takeaway:* once sharing and nesting matter, access becomes a graph. Plan for relationships, caching and the "which objects can this user see" question. See [ReBAC and policy engines](./rebac-and-policy-engines.md). From search-result excerpts of the paper.

**The agent that did what the asker could not (an illustration).** An internal assistant is given a service key that can read the whole company wiki. A junior employee asks it about pay bands. It answers from a restricted page. Nothing was hacked. The agent had more access than the person asking. 🎯 *Takeaway:* an agent must carry the user's authority, not its own. See [access control for AI agents](./access-control-for-ai-agents.md). This story is invented.

**The role list that grew to thirty-one (an illustration).** A document product launches with four roles, then adds a role for each department and region. By year four nobody can say what `viewer-legal` allows. 🎯 *Takeaway:* department and region are attributes, not jobs. Keep a short role list and add rules for the rest. See [RBAC](./rbac-roles-groups-and-where-it-breaks.md). This story is invented.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Authentication, authorization and the access-control model](./authentication-authorization-and-the-access-control-model.md) | Authentication says who. Authorization decides what. Deny by default, enforce on the server, log every decision. | Where is this rule enforced, and what is the default? |
| [OAuth 2.0, OpenID Connect and tokens](./oauth-openid-connect-and-tokens.md) | Tokens carry identity and permission. Each has an audience and a lifetime. | If we remove access now, how long can an existing token still work? |
| [RBAC](./rbac-roles-groups-and-where-it-breaks.md) | Roles are jobs. They break on objects and context, and they grow. | Can a new admin say what each role allows? |
| [ABAC](./abac-deciding-with-attributes-and-context.md) | Decide from attributes of subject, object, action and context. Treat attributes as managed data. | Who sets each attribute, and can a user change it? |
| [ReBAC and policy engines](./rebac-and-policy-engines.md) | Sharing is a graph. Policy can live in one reviewed place. | If someone is removed from a folder, how fast do they lose access to what is in it? |
| [Keycloak: realms, clients, roles, groups and tokens](./keycloak-realms-clients-roles-groups-and-tokens.md) | Keycloak holds identity. Getting roles and attributes into tokens is a separate, deliberate step. | What does each of our tokens carry, and who owns running the server? |
| [Keycloak Authorization Services](./keycloak-authorization-services.md) | Resources, scopes, policies and permissions. Strategy matters. Deny by default. | Which rules live in Keycloak, which in code, and what happens when Keycloak is down? |
| [Access control for AI agents](./access-control-for-ai-agents.md) | An agent carries the user's authority and no more. | What is the most a tricked agent could read or change? |

**The through-line:** every access decision has the same four inputs: who, what, on which object, and under what conditions. The models differ in which inputs they use and where the rule lives. In this module's view, many failures are not clever attacks. They are a missing check, a default that allows, a token that outlives access, an attribute a user can edit, or an agent with more power than its user. This module stays at the decision level. Neighbouring lessons carry the depth on tools, memory, tenants and agent safety.

> **Walk-away question:** *"For our most sensitive object: who may read and change it, where is that decided, what is the default when no rule matches, how fast does a removal take effect, and could an AI agent acting for a low-privilege user reach it?"*

If yes, access is a feature you can stand behind. If no, you know which lesson to reread.

## Test yourself

1. **What is the difference between authentication and authorization?**
   <details><summary>Answer</summary>Authentication proves who someone is. Authorization decides what that verified person may do on a specific object. A verified user is not a permitted user. (<a href="./authentication-authorization-and-the-access-control-model.md">Lesson 1</a>)</details>
2. **Name the four parts of an authorization system and what each does.**
   <details><summary>Answer</summary>The enforcement point stops or allows the request. The decision point evaluates the policy. The information point supplies attributes and relationships. The administration point is where policy is written and changed. (<a href="./authentication-authorization-and-the-access-control-model.md">Lesson 1</a>)</details>
3. **Which token should an API accept as proof of access, and which should it not?**
   <details><summary>Answer</summary>It should accept an access token issued for it. It should not accept an ID token, which is for the client app. It must check signature, issuer, audience, expiry and scope. (<a href="./oauth-openid-connect-and-tokens.md">Lesson 2</a>)</details>
4. **Why does token lifetime matter when someone loses access?**
   <details><summary>Answer</summary>A signed token keeps working until it expires. The lifetime sets how long a removed person can still act, unless the API checks the server live for risky actions. (<a href="./oauth-openid-connect-and-tokens.md">Lesson 2</a>)</details>
5. **What is role explosion, and how do you avoid it?**
   <details><summary>Answer</summary>Roles multiply as each exception becomes a new role. Avoid it by keeping a short list of job roles and moving object and context limits into attribute or relationship rules. (<a href="./rbac-roles-groups-and-where-it-breaks.md">Lesson 3</a>)</details>
6. **A rule says "editors may edit reports in their own department." The user has no department attribute. What should happen?**
   <details><summary>Answer</summary>The request is denied. A missing attribute must never be treated as allow, and the default when no rule matches is deny. (<a href="./abac-deciding-with-attributes-and-context.md">Lesson 4</a>)</details>
7. **When does ReBAC fit better than RBAC or ABAC?**
   <details><summary>Answer</summary>When access follows sharing, nesting and inheritance, such as folders, groups and ownership chains. A path of stored relationships grants access, and removing one link removes everything that depended on it. (<a href="./rebac-and-policy-engines.md">Lesson 5</a>)</details>
8. **In Keycloak, a custom user attribute is set but does not appear in the token. Why?**
   <details><summary>Answer</summary>By default Keycloak only recognises attributes declared in the realm's user profile, so an undeclared attribute is ignored. It must be declared, and a mapper must put it in the token. (<a href="./keycloak-realms-clients-roles-groups-and-tokens.md">Lesson 6</a>)</details>
9. **A permission has two policies: "is editor" and "in finance." Under which decision strategy does a user who is only an editor get access?**
   <details><summary>Answer</summary>Under the affirmative strategy, where one passing policy is enough. Under unanimous, the default, all policies must pass, so that user is denied. (<a href="./keycloak-authorization-services.md">Lesson 7</a>)</details>
10. **Why should an agent use the user's identity, and not one powerful service key, when answering user questions?**
    <details><summary>Answer</summary>A service key gives every user the agent's full reach, which is the confused deputy problem. With the user's identity the decision is made as that user, so the agent can do no more than they can. (<a href="./access-control-for-ai-agents.md">Lesson 8</a>)</details>

## Sources

- OWASP, *API Security Top 10, 2023*, API1 Broken Object Level Authorization. Described from search-result summaries. The page could not be opened.
- US Office of the Comptroller of the Currency, Capital One enforcement action (Aug 2020, $80 million civil money penalty); press and law-firm coverage of the 2019 incident. Described from search-result excerpts. The OCC order could not be opened.
- OpenAI, *March 20 ChatGPT outage: here's what happened* (Mar 2023). Search-result excerpts only; the page could not be opened.
- Pang et al., *Zanzibar: Google's Consistent, Global Authorization System*, USENIX ATC 2019. Search-result excerpts only.
- The pay-band assistant and the thirty-one role stories are invented illustrations.

---

← Back to [module overview](./README.md)
