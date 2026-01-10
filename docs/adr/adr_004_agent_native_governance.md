# ADR 004: Agent-Native Governance Files

## Status
Accepted

## Context
AI coding agents (Copilot, Cursor, Windsurf) need structured context to:
- Understand project architecture without extensive exploration
- Follow consistent coding standards
- Avoid common mistakes (secrets, wrong patterns)

## Decision
Implement three-tier agent context system:

### Tier 1: AGENTS.md (Root)
- **Purpose:** Universal entry point for all agents
- **Content:** Codebase map, command palette, file header template
- **Location:** Repository root

### Tier 2: .cursorrules
- **Purpose:** IDE-specific rules for Cursor
- **Content:** Stack definition, style rules, boundaries
- **Location:** Repository root

### Tier 3: .github/copilot-instructions.md
- **Purpose:** GitHub Copilot-specific context
- **Content:** High-density architecture summary
- **Location:** .github/ directory

### File Header Template
All source files should reference AGENTS.md:
```python
# See AGENTS.md for project context and conventions
```

## Consequences
- **Positive:** Agents produce consistent, project-aligned code on first attempt
- **Negative:** Additional files to maintain
- **Tradeoff:** Three files covers major agent ecosystems without over-engineering
