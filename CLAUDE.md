# CLAUDE.md - AI Assistant Integration Guide

## Overview
This document provides guidance for using AI assistants (like Claude) effectively in the Hackathon Todo Application development.

## When to Use AI Assistants

### Appropriate Use Cases

#### 1. Code Generation
- Boilerplate code creation
- Component template generation
- Configuration file creation
- Documentation generation

#### 2. Code Review & Analysis
- Code style suggestions
- Performance improvement identification
- Security vulnerability detection
- Best practice recommendations

#### 3. Documentation
- API documentation
- Setup guides
- Troubleshooting guides
- Architecture documentation

#### 4. Problem-Solving
- Debugging complex issues
- Architecture decisions
- Technology selection
- Design pattern recommendations

#### 5. Learning & Training
- Explaining concepts
- Technology tutorials
- Best practices overview
- Framework/library guidance

### Inappropriate Use Cases

#### 1. Bypassing SDD Process
- Implementing without specifications
- Creating code without Task IDs
- Skipping planning phase
- Ignoring acceptance criteria

#### 2. Replacing Human Judgment
- Critical security decisions
- User experience decisions
- Data retention policies
- Business logic pivots

#### 3. Autonomous Development
- Full feature implementation without review
- Database schema changes without testing
- Production deployments
- Unreviewed API changes

## Working with AI Assistants

### Best Practices

#### 1. Provide Clear Context
```
GOOD:
"I need to implement the POST /todos endpoint specification
as defined in specs/phase2/specify.md. The endpoint should
create a new todo with validation and return a 201 response.
Here's my current code: [code snippet]"

POOR:
"Can you code a todo creation endpoint?"
```

#### 2. Use Specifications as Source of Truth
```
GOOD:
"According to specs/phase2/specify.md, the response should
include pagination metadata. My current implementation is
missing this. How can I add it?"

POOR:
"Make the response return more data"
```

#### 3. Include Task ID References
```
GOOD:
"For PHASE2-004 (Todo CRUD Operations), I'm implementing
the DELETE endpoint. I need help with error handling."

POOR:
"I'm deleting todos, help me with this"
```

#### 4. Request Specific Assistance
```
GOOD:
"Can you review this code for security vulnerabilities
related to input validation?"

POOR:
"Is this code good?"
```

### Code Generation Guidelines

#### When AI Creates Code
1. Always review the generated code thoroughly
2. Verify it matches specifications exactly
3. Check for security vulnerabilities
4. Test with unit tests before committing
5. Include Task ID in commit message

#### Code Ownership
```
YOUR RESPONSIBILITY:
- ✓ Understanding the code
- ✓ Testing thoroughly
- ✓ Handling edge cases
- ✓ Security review
- ✓ Performance verification

ASSISTANT RESPONSIBILITY:
- ✗ Code quality guarantee
- ✗ Security verification
- ✗ Performance optimization
- ✗ Test completeness
- ✗ Production readiness
```

### Documentation Guidelines

#### AI-Generated Documentation
- Always verify factual accuracy
- Include examples where helpful
- Ensure consistency with codebase
- Test instructions before publishing
- Update documentation when code changes

#### Documentation Standards
```
GOOD documentation:
- Clear and concise
- Examples provided
- Links to relevant specs
- Covers edge cases
- Regular updates

POOR documentation:
- Generic/vague
- Incomplete
- Outdated
- No examples
- Inconsistent
```

## Collaboration Framework

### AI Assistant Role in SDD

#### Constitution Phase
- AI can help draft vision and goals
- Assists with writing clear objectives
- Provides best practice examples
- Creates structured documents

#### Specification Phase
- AI generates specification templates
- Helps with technical details
- Provides comprehensive examples
- Ensures completeness

#### Planning Phase
- AI assists with implementation plans
- Helps break down tasks
- Identifies dependencies
- Estimates subtask breakdown

#### Implementation Phase
- AI generates code based on specs
- Reviews code for quality
- Assists with debugging
- Helps with documentation

#### Verification Phase
- AI helps verify acceptance criteria
- Checks for completeness
- Reviews documentation
- Assists with testing

### Verification Checklist

Before Committing AI-Generated Code:
```
✓ Code reviewed manually
✓ Matches specification exactly
✓ Unit tests pass
✓ No security issues
✓ No performance problems
✓ Follows code standards
✓ Task ID referenced
✓ Comments clear and helpful
✓ No dead code or TODOs
✓ Database migrations tested
```

## Security Considerations

### Code Security

#### Red Flags in AI-Generated Code
- Missing input validation
- SQL injection vulnerabilities
- Hardcoded secrets/credentials
- Missing authentication checks
- Insecure cryptography
- Missing error handling
- Race conditions

#### Security Review Process
1. Use automated security scanners
2. Manual code review for logic
3. Security expert review for sensitive areas
4. Penetration testing for authentication
5. Dependency vulnerability scanning

### Data Privacy
- Never share customer data with AI
- Don't paste sensitive configuration
- Sanitize error messages and logs
- Verify no credentials in code snippets

## Quality Assurance

### Testing AI-Generated Code

#### Unit Testing
```javascript
// AI generates the function
function calculateTodoStats(todos) {
  // Generated code
}

// YOU must write tests
describe('calculateTodoStats', () => {
  test('returns correct count of completed todos', () => {
    // Test specification adherence
  });

  test('handles empty array', () => {
    // Test edge case
  });

  test('handles null values', () => {
    // Test error condition
  });
});
```

#### Integration Testing
- Test with actual database
- Test with API endpoints
- Test with frontend integration
- Test error scenarios
- Test performance with scale

### Performance Verification
- Profile generated code
- Check for N+1 queries
- Verify algorithm efficiency
- Test with realistic data volumes
- Compare with specification requirements

## Communication with AI

### Effective Prompting

#### Good Prompts
```
"I need to implement the todo detail endpoint as specified in
specs/phase2/specify.md lines 145-170. The endpoint should:
1. Validate the user owns the todo
2. Return 404 if not found
3. Return 403 if not authorized
4. Return 200 with todo details

Here's my current code: [code]
Can you identify security issues?"
```

#### Poor Prompts
```
"Make an endpoint for getting a todo"
"Fix my code"
"What's the best way to do this?"
```

### Handling AI Mistakes

When AI Misunderstands:
```
RESPONSE:
"The generated code doesn't match specification requirement
on line X. The spec requires Y, but the code implements Z.
Can you fix this specifically?"

NOT:
"This is wrong"
```

When AI Suggests Out-of-Spec Changes:
```
RESPONSE:
"This suggestion is good, but it's outside the current
specification (PHASE2-004). We'd need to go through the
specification change process first. For now, can we stick
to the current specification?"

NOT:
"Just follow the spec"
```

## Documenting AI Assistance

### Git Commits
```
feat(auth): implement JWT token refresh PHASE2-002

- Add token refresh endpoint per specification
- Implement refresh token validation
- Add rotation of refresh tokens

Generated with Claude AI - reviewed for security,
tested with unit tests, verified against spec

Task-ID: PHASE2-002
```

### Code Comments
```javascript
// Generated by AI, reviewed for security and spec compliance
// Validates token signature and expiration
function validateToken(token) {
  // Implementation
}
```

### Documentation
```markdown
## Implementation Notes

This component was initially generated with AI assistance
and thoroughly reviewed for:
- Specification compliance (PHASE3-005)
- Accessibility standards (WCAG 2.1 AA)
- Performance (Lighthouse ≥85)
- Security (no XSS, CSRF protection)
```

## Learning & Development

### Using AI for Skill Building
- Explain concepts you don't understand
- Ask for learning resources
- Request code walkthroughs
- Ask for best practice explanations
- Request architectural guidance

### Effective Learning
```
GOOD:
"Can you explain how JWT token refresh works and why it's
necessary? I want to understand before implementing."

POOR:
"Just generate the code for token refresh"
```

## Limitations & Disclaimers

### What AI Cannot Guarantee
- ✗ Code is 100% bug-free
- ✗ Security vulnerabilities found
- ✗ Performance is optimal
- ✗ Specifications fully understood
- ✗ Edge cases handled
- ✗ Test coverage complete

### Your Responsibility
- ✓ Manual code review
- ✓ Security verification
- ✓ Test writing and verification
- ✓ Specification compliance
- ✓ Edge case handling
- ✓ Performance optimization

## Escalation Path

### When to Escalate
1. AI cannot understand specification
2. AI generates code that violates specification
3. Security concerns about AI-generated code
4. Performance issues in AI code
5. Recurring misunderstandings

### Escalation Process
1. Document the issue clearly
2. Include relevant specifications
3. Provide code snippets
4. Request human review
5. Adjust future interactions based on feedback

## Success Metrics

### Healthy AI Integration
- Code quality maintained or improved
- Specification adherence 100%
- Security issues caught in review
- Team productivity increased
- Learning outcomes achieved
- Zero unreviewed code in production

### Red Flags
- AI code committed without review
- Bypassing specification process
- Ignoring AI mistakes
- Over-reliance on generation
- Security issues from AI code
- Team unable to understand AI code
