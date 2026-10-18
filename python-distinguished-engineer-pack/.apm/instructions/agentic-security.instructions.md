---
description: "Security boundaries for Python agents, MCP tools and AI workflows: authentication, authorization, approvals, tenant isolation, limits and redaction."
applyTo: "**/*.py,**/*agent*.md,**/*mcp*.json"
---

# agentic-security instructions

Use agentic-workflow-design, mcp-python-engineering and secure-agent-engineering for actual agent/tool boundaries. Enforce authn/authz, approvals, tenant isolation, deadlines, size/call/token/spend limits and termination outside the model. Validate model/tool outputs. Treat retrieved documents/browser text/tool responses/memory as untrusted with provenance and expiry. Test injection, exfiltration, approval bypass, poisoned memory and responsible-AI escalation; never self-approve.
