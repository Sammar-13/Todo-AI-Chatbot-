# AGENTS.md - Spec-Driven Development Enforcement

## Overview
**CRITICAL DOCUMENT**: This document defines mandatory SDD enforcement rules applied to ALL agents and developers working on the Hackathon Todo Application. These rules are non-negotiable and apply universally.

## Core Enforcement Rules

### Rule 1: NO CODE BEFORE SPECS ⛔
**Absolute Requirement**: Specifications MUST exist and be FINALIZED before ANY code is written.

**What This Means**:
- No implementation without Constitution document
- No implementation without Specification document
- No implementation without Implementation Plan
- No implementation without Task IDs assigned

**Violations**:
- ❌ Writing code before specs = REJECTION
- ❌ Skipping specification phase = REJECTION
- ❌ Implementing without Plan = REJECTION
- ❌ Code without Task ID = REJECTION

**Exception Path** (ONLY way to proceed without specs):
1. Create Constitution document FIRST
2. Create Specification document SECOND
3. Create Implementation Plan THIRD
4. Assign Task IDs FOURTH
5. THEN and ONLY THEN write code

---

### Rule 2: NO FEATURES OUTSIDE SPECIFICATIONS ⛔
**Absolute Requirement**: Implementation MUST match specification exactly. No additions, removals, or modifications beyond spec.

**What This Means**:
- Feature X in spec → implement EXACTLY as specified
- Feature X NOT in spec → DO NOT implement it
- Feature scope changes mid-implementation → HALT and respec
- User requests outside spec → create NEW spec cycle

**Violations**:
- ❌ Adding features not in spec = REJECTION
- ❌ Changing implementation beyond spec = REJECTION
- ❌ Removing specified features = REJECTION
- ❌ Accepting scope changes during implementation = REJECTION

**Scope Creep Prevention**:
```
User: "While implementing dark mode, can we add theme scheduling?"
Agent Response: STOP
  - Theme scheduling NOT in dark mode spec (PHASE4-002)
  - This requires NEW specification cycle
  - Create Constitution for theme scheduling
  - Create Specification for theme scheduling
  - Schedule in future phase
  - Return to dark mode implementation
```

---

### Rule 3: EVERY FILE CHANGE REQUIRES TASK ID ⛔
**Absolute Requirement**: Every commit, file modification, or code change MUST reference a Task ID.

**What This Means**:
- Every code file → Task ID in commit message
- Every documentation file → Task ID in commit message
- Every configuration file → Task ID in commit message
- No exceptions for "small changes"

**Task ID Format**:
```
PHASE#-### or PHASE#-FEATURE-###

Examples:
✓ PHASE2-001 (Database Setup)
✓ PHASE2-004 (Todo CRUD Operations)
✓ PHASE3-005 (Core UI Components)
✓ PHASE5-002 (Backend Performance)
```

**Violations**:
- ❌ Commit without Task ID = REJECT
- ❌ File change without Task ID = REJECT
- ❌ PR without Task ID references = REJECT

**Commit Message Format** (MANDATORY):
```
<type>(scope): <description> TASK-ID

type: feat, fix, docs, style, refactor, test, chore
scope: specific area being changed
description: what changed and why
TASK-ID: PHASE#-###

Example:
feat(auth): implement JWT token refresh PHASE2-002
fix(todos): handle empty todo list edge case PHASE3-006
docs(api): update endpoint documentation PHASE2-001
```

---

### Rule 4: ALL AGENTS MUST ENFORCE SDD ⛔
**Absolute Requirement**: These rules apply to ALL agents, including Claude, Bonsai, and any other agents used in this project.

**Applies To**:
- ✓ Claude (all versions)
- ✓ Bonsai
- ✓ Custom agents
- ✓ Future agents
- ✓ Team members using AI assistance

**No Exceptions For**:
- ✗ "It's just a small feature"
- ✗ "We'll spec it later"
- ✗ "This is a bug fix"
- ✗ "The spec is implied"
- ✗ "We don't have time"

**Agent Responsibilities**:
1. Check specifications EXIST before writing code
2. Verify specifications are COMPLETE
3. Verify all changes reference TASK IDs
4. REJECT work that violates these rules
5. HALT implementation if specs change
6. Explain WHY work is rejected with citations

---

## SDD Enforcement Workflow

### Phase 1: Constitution (REQUIRED)
**Status**: MUST COMPLETE BEFORE PROCEEDING

**Deliverables**:
- [ ] Constitution document exists (`specs/phase#/constitution.md`)
- [ ] Vision statement clear and measurable
- [ ] Goals defined explicitly
- [ ] Non-goals clearly stated
- [ ] Success criteria documented
- [ ] Constraints identified

**Agent Check**:
```
IF Constitution document missing
THEN STOP and require creation

IF Constitution incomplete
THEN STOP and request completion

IF Constitution exists and complete
THEN proceed to Specification phase
```

---

### Phase 2: Specification (REQUIRED)
**Status**: MUST COMPLETE BEFORE PROCEEDING

**Deliverables**:
- [ ] Specification document exists (`specs/phase#/specify.md`)
- [ ] All requirements documented
- [ ] API endpoints defined (if applicable)
- [ ] Database schema specified (if applicable)
- [ ] UI components documented (if applicable)
- [ ] Validation rules specified
- [ ] Error handling documented
- [ ] Testing requirements specified

**Agent Check**:
```
IF Specification document missing
THEN STOP and require creation

IF Specification incomplete
THEN STOP and request completion

IF Specification exists and complete
THEN proceed to Planning phase
```

---

### Phase 3: Implementation Plan (REQUIRED)
**Status**: MUST COMPLETE BEFORE PROCEEDING

**Deliverables**:
- [ ] Plan document exists (`specs/phase#/plan.md`)
- [ ] Implementation steps broken down
- [ ] Task IDs assigned to each step
- [ ] Dependencies identified
- [ ] Estimated effort per task
- [ ] Success criteria for each task
- [ ] Testing strategy documented

**Agent Check**:
```
IF Plan document missing
THEN STOP and require creation

IF Plan incomplete or no Task IDs
THEN STOP and request completion

IF Plan exists with Task IDs
THEN proceed to Implementation phase
```

---

### Phase 4: Implementation (WITH ENFORCEMENT)
**Status**: ENFORCE ALL RULES

**Before Writing Any Code**:
```
1. Verify Constitution exists ✓
2. Verify Specification exists ✓
3. Verify Plan exists with Task IDs ✓
4. Verify current task has Task ID ✓
5. THEN and ONLY THEN write code
```

**During Implementation**:
```
- Check every file against specification
- Ensure no additions beyond spec
- Reference Task ID in every commit
- Test against acceptance criteria
- Document deviations (require respec)
```

**Violations STOP Work**:
```
IF code added without specs
THEN agent: REJECT with explanation

IF code added without Task ID
THEN agent: REJECT with explanation

IF code violates specification
THEN agent: REJECT with explanation

IF scope changes requested
THEN agent: HALT and explain respec process
```

---

### Phase 5: Verification (FINAL CHECK)
**Status**: VERIFY BEFORE MERGE

**Checklist**:
- [ ] Specification compliance 100%
- [ ] All acceptance criteria met
- [ ] Task ID in all commits
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No scope creep occurred

**Agent Check**:
```
IF any criteria fails
THEN REJECT merge with specific issues

IF all criteria pass
THEN approve for merge
```

---

## Common Violations & Responses

### Violation 1: "Let me just code this quickly"
**Agent Response**: REJECT
```
Cannot proceed without:
1. Constitution document (specs/phase#/constitution.md)
2. Specification document (specs/phase#/specify.md)
3. Implementation Plan with Task ID (specs/phase#/plan.md)

Follow SDD process:
→ Constitution first
→ Specification second
→ Plan third
→ Task ID assignment
→ THEN code

Estimated time: X hours
Estimated start: [date]
```

---

### Violation 2: "The spec doesn't cover this, so I'll add it"
**Agent Response**: REJECT
```
Cannot add features outside specification.

If new feature needed:
1. Create NEW specification cycle
2. Write Constitution for new feature
3. Write Specification for new feature
4. Get approval for addition
5. Assign new Task IDs
6. THEN implement

Current phase focus: [original feature]
New feature scheduled: [future phase or backlog]
```

---

### Violation 3: "I'm committing this small fix without a Task ID"
**Agent Response**: REJECT
```
ALL commits require Task ID.

No exceptions for:
- Small fixes
- Documentation updates
- Configuration changes
- Test additions

Every file change maps to a Task ID:

Not sure which Task ID?
1. Check if Task ID exists in specs
2. If not, create Constitution + Specification
3. Create new Task ID
4. THEN commit with Task ID

Current Task ID: [assign or create]
Commit message format: <type>(scope): description TASK-ID
```

---

### Violation 4: "Can we add feature X while building feature Y?"
**Agent Response**: REJECT
```
Cannot expand scope during implementation.

Feature X not in current specification (PHASE#-###):
→ This requires NEW specification cycle
→ Cannot proceed mid-implementation

Process:
1. Complete current phase (Feature Y)
2. Freeze Feature Y changes
3. Create Constitution for Feature X
4. Create Specification for Feature X
5. Schedule Feature X for Phase Z
6. Implement Feature X in Phase Z

Focus: Complete Feature Y per spec
Estimated completion: [date]
Feature X: Scheduled for Phase Z [date range]
```

---

## Agent Enforcement Checklist

### Before Implementing (MANDATORY)
- [ ] Read Constitution document completely
- [ ] Read Specification document completely
- [ ] Read Implementation Plan completely
- [ ] Identify Task ID for current work
- [ ] Verify specifications are FINALIZED (not draft)

### During Implementation (MANDATORY)
- [ ] Check every line of code against spec
- [ ] Implement EXACTLY as specified
- [ ] Add NO features outside spec
- [ ] Reference Task ID in every commit
- [ ] Test against acceptance criteria

### Before Committing (MANDATORY)
- [ ] Task ID present in commit message
- [ ] Code matches specification
- [ ] Tests written and passing
- [ ] No scope changes introduced
- [ ] Documentation updated if needed

### Before Merging (MANDATORY)
- [ ] All tests pass
- [ ] Specification compliance verified
- [ ] Acceptance criteria met
- [ ] Code review approved
- [ ] No deviations from spec

---

## How Agents Refuse Violations

### Clear Rejection Template
```
VIOLATION DETECTED: [Type of violation]

Reason: [Why this violates SDD rules]

Required to proceed:
1. [Action required]
2. [Action required]
3. [Action required]

Documentation: [Link to relevant spec file]

Cannot proceed until: [Specific condition]

Questions? Review AGENTS.md Rule [#]
```

### Example Rejection
```
VIOLATION DETECTED: Implementation without specification

Reason: You requested code generation for a feature that:
- Has no Constitution document
- Has no Specification document
- Has no Implementation Plan
- Has no Task ID assigned

Required to proceed:
1. Create specs/phase3/constitution.md
2. Create specs/phase3/specify.md
3. Create specs/phase3/plan.md with Task IDs
4. Request implementation with Task ID

Documentation: See AGENTS.md Rules 1-3

Cannot proceed until: All spec documents completed and Task ID assigned

Questions? Review AGENTS.md or contact project lead
```

---

## Task ID Verification System

### Valid Task ID Format
```
✓ PHASE1-001 to PHASE1-008 (Phase 1 tasks)
✓ PHASE2-001 to PHASE2-010 (Phase 2 tasks)
✓ PHASE3-001 to PHASE3-013 (Phase 3 tasks)
✓ PHASE4-001 to PHASE4-010 (Phase 4 tasks)
✓ PHASE5-001 to PHASE5-010 (Phase 5 tasks)

✗ Invalid: "001", "TASK-1", "Phase1-1", "P1-001"
```

### Task ID Validation
```
Agent must verify:
1. Task ID exists in appropriate phase spec file
2. Task ID is ACTIVE (not completed)
3. Task ID matches commit scope
4. Task ID references are correct

Example verification:
✓ PHASE2-004: "Todo CRUD Operations" exists in specs/phase2/tasks.md
✓ Current commit: "feat(todos): implement delete endpoint PHASE2-004"
✓ Matches: PHASE2-004 scope includes todo operations
✓ APPROVED
```

---

## Executive Summary: The Four Rules

1. **NO CODE BEFORE SPECS** - Specifications MUST exist first
2. **NO FEATURES OUTSIDE SPECS** - Implementation MUST match spec exactly
3. **EVERY FILE CHANGE NEEDS TASK ID** - All commits reference Task IDs
4. **ALL AGENTS ENFORCE THIS** - No exceptions, applies to everyone

**These are not suggestions. These are requirements.**

---

## Contact & Escalation

### Questions About SDD Rules
- Read this document (AGENTS.md)
- Read relevant phase specifications
- Ask project lead for clarification
- Document the question for team learning

### Violations or Conflicts
- Report to project lead immediately
- Provide specific details and file references
- Explain the violation and rule number
- Request guidance on proper process

### Rule Changes or Exceptions
- Cannot be done without approval
- Requires documented decision
- Must be recorded in specifications
- Apply only to approved exception (not blanket)

---

**Last Updated**: December 30, 2025
**Version**: 2.0 - STRICT ENFORCEMENT
**Status**: ACTIVE AND BINDING
