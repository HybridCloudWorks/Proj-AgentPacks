# Safe Helper Tools

The pack's helper tools are local and conservative:

- `tooling/repository_inventory.py` emits a bounded, read-only repository inventory.
- `tooling/command_guard.py` rejects common push, merge, deploy, apply, delete, publish, and external-write commands.
- `tooling/validate_engineering_report.py` checks the evidence completion contract.
- `tooling/validate_evaluation_scenario.py` checks evaluation scenario shape.

They do not replace host permissions, repository policy, security review, or human approval.
