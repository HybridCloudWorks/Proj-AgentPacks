---
name: azure-data-and-application-patterns
description: Designs Azure data platforms and application architectures with explicit consistency, partitioning, integration, privacy, lifecycle, and operational trade-offs.
---

# Azure Data and Application Patterns

Start from access patterns, consistency, transactions, retention, recovery, data classification, residency, throughput, latency, and ownership. Select relational, NoSQL, object, file, analytics, and event services from those requirements rather than product catalogs.

Cover Azure SQL, PostgreSQL/MySQL, Cosmos DB, Storage, Data Lake, Event Hubs, Service Bus, Event Grid, Data Factory, Fabric/Databricks/AML where relevant. State partition keys, replication, failover, backup, encryption, private access, schema evolution, and deletion/retention behavior.

For applications, make synchronous versus asynchronous boundaries, idempotency, retries, poison messages, caching, deployment compatibility, and observability explicit. Never call a data design compliant or lossless without tested evidence.
