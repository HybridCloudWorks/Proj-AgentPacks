# Google Cloud knowledge and integration contract

## Command-line tools

`gcloud`, `bq`, `gcloud storage`, `gsutil`, `kubectl` and Terraform or OpenTofu are used only if they are already installed and authenticated by the user. The pack installs none of them. Every leaf command is validated with its help before first use, every resource command carries an explicit project or scope and location, and output is reduced with filters, projections and limits. Mutating, IAM, API-enablement, billing, organization, KMS and deployment commands are Level 2.

## Identity

The preferred identity for discovery is a dedicated service account with viewer-type roles that the user impersonates, so the agent's actions are scoped and audited separately from the human's broader access. Service account keys are never requested, created or accepted. Workload Identity Federation is the pattern for CI pipelines that plan infrastructure.

## MCP servers

Google publishes MCP servers for several products (for example Cloud Monitoring, Cloud Logging, BigQuery, GKE and Data Lineage) and a Developer Knowledge server for documentation search. The pack configures none of them and never edits client MCP configuration files. A skill uses an MCP server only when the client already has it connected and its identity and scope are known; otherwise it uses the CLI or official documentation. An MCP tool's self-description (for example a read-only hint) helps choose tools; it is not a permission check, so the approval levels apply to MCP calls exactly as to CLI commands.

## Documentation and product facts

Official Google Cloud documentation is the authority for product status, limits, SLAs, pricing and regional availability. The pack hard-codes no prices and few limits, and the skills tell the model to verify them at task time and to mark anything it could not verify. Product names changed in 2026 (Vertex AI to Gemini Enterprise Agent Platform, Dataplex to Knowledge Catalog, Dataproc Serverless to Managed Service for Apache Spark, BigLake to Lakehouse for Apache Iceberg) while API names, IAM roles and Terraform resources often kept their old identifiers.

## What is not configured

No organization, project, billing account, region, credential, MCP registration or deployment target is configured by the pack. The user supplies them for each task; the pack never ships made-up values for them in anything that could be run.
