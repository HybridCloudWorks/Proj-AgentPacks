# Worked example: a remote MCP server for support staff

Request: "Expose order lookup and refunds to our support assistant as an MCP server on Cloudflare, with company SSO."

1. Contract first (cloudflare-agents-and-ai). Two tools: `lookup_order` (read, any support agent) and `refund_order` (consequential, only the `support-leads` group, amount capped, human approval required). Inputs are strict schemas; outputs are bounded and exclude card data. Budgets: request timeout, maximum results, per-user rate limit.
2. Identity. OAuth through the Workers OAuth provider library in front of the server, federated to the company identity provider; redirect URIs validated; the authenticated identity and group claims are passed to the server as props. Authorization for each tool reads those props, never a `user` argument the model could fill in.
3. Implementation. An `McpAgent` class with its Durable Object binding and a `new_sqlite_classes` migration; Streamable HTTP transport; the refund tool returns a pending approval record, and a separate approval step (a person in the support console) executes the refund with the approved parameters only. No generic fetch or SQL tool is exposed.
4. Tests with fakes. Initialize and list tools, call each tool with valid, malformed and oversized arguments, call `refund_order` as a non-lead (denied), call it with an injected instruction in an order note (treated as data, no action), and exhaust the rate limit. All run locally against the Worker in the Vitest pool with the order API mocked.
5. Before release. Registering the OAuth client with the identity provider, creating the Durable Object namespace by deploying, and connecting the support assistant to the server are Level 2 steps listed for cloudflare-change-control.

Report: CHANGE_PREPARED_NOT_APPLIED. Unverified: real identity-provider claims, production latency, and the assistant's behavior with the live server.
