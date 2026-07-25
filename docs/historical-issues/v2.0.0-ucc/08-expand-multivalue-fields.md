# Expand Splunk multivalue fields

**Suggested labels:** enhancement, data-model  
**Status:** Resolved in 2.1.0

## Context

A list-valued Splunk field is passed as one value.

## Acceptance criteria

- Each non-empty member becomes its own MISP attribute.
- Scalar behavior is unchanged.

## Resolution

The final pusher normalizes scalar and multivalue inputs.
