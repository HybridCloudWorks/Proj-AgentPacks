# MCP Routing

Use AWS Knowledge MCP for current AWS docs, architecture guidance, Well-Architected content, API references, agent skills, and Region lists. Use AWS MCP Server/Agent Toolkit API tools only for authorized account interactions. Use AWS IaC MCP for CloudFormation/CDK/IaC guidance. Use pricing, CloudWatch, CloudTrail, IAM, security, and service-specific MCP servers only when the host has them and the task benefits from them.

The official AWS Knowledge endpoint is remote and does not require an AWS account, but it does require network access and is rate-limited. Remote MCP support varies by client. Never claim a tool was called if it was unavailable.

Before a live call, confirm: client/server identity, transport, profile or role, account, Region, read/write mode, requested operation, sensitive data exposure, approval requirement, and rollback. Prefer read-only calls for discovery and architecture review.
