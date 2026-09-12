# Student Onboarding — DCYN Logic & Validation

## 1. Purpose

This document defines the proposed deterministic validation and
DCYN (Yes/No) decision logic for the student onboarding process.

The hiring brief requires incoming student onboarding data to be
deconstructed into binary decision logic and validated through
Django REST Framework to eliminate human judgment.

## 2. Source Constraint

The hiring brief does not provide a concrete student onboarding
JSON payload or field-level validation limits.

Therefore, the schema, validation limits, and decision rules below
are proposed engineering rules for this implementation. They are
not presented as requirements supplied by HabotConnect.

## 3. Proposed Input Schema

| Field | Type | Required | Validation |
|---|---|---|---|
| student_name | string | Yes | 2–100 characters |
| email | string | Yes | Valid email, maximum 254 characters |
| phone | string | Yes | Exactly 10 digits |
| age | integer | Yes | 18–60 |
| has_passport | boolean | Yes | true/false only |
| has_academic_documents | boolean | Yes | true/false only |
| english_proficiency | boolean | Yes | true/false only |
| willing_to_relocate | boolean | Yes | true/false only |
| has_relevant_experience | boolean | Yes | true/false only |

## 4. DCYN Decision Logic

### DCYN-1 = Required Information

Is all required onboarding information present?

- YES → Continue to DCYN-2
- NO → Reject and quarantine record

### DCYN-2 = Data Type

Are all fields supplied using the expected data type?

- YES → Continue to DCYN-3
- NO → Reject and quarantine record

### DCYN-3 = Field Validation

Do all values satisfy their defined validation constraints?

- YES → Continue to DCYN-4
- NO → Reject and quarantine record

### DCYN-4 = Binary Decision

Are all DCYN decision fields explicitly represented as
boolean Yes/No values?

- YES → Continue to DCYN-5
- NO → Reject and quarantine record

### DCYN-5 = Final Onboarding Decision

Does the record satisfy all mandatory onboarding conditions?

- YES → Accept and continue processing
- NO → Reject and quarantine record

## 5. Binary Decision Fields

The following fields are treated as deterministic Yes/No decisions:

- has_passport
- has_academic_documents
- english_proficiency
- willing_to_relocate
- has_relevant_experience

`true` represents YES.

`false` represents NO.

No third state such as "maybe", "unknown", or free-text
interpretation is accepted.

## 6. Mistake-Proofing Rules

The implementation must reject:

- Missing required fields
- Unexpected fields where strict validation is enabled
- Incorrect data types
- Invalid email addresses
- Phone numbers that are not exactly 10 digits
- Ages outside the defined range
- Strings outside their defined length limits
- Non-boolean values for DCYN fields

The system must not rely on manual interpretation of submitted
values.

## 7. Processing Outcome

VALID INPUT

→ Accept onboarding record

→ Continue downstream processing

→ Write validated record to D1

INVALID INPUT

→ Reject onboarding record

→ Return validation errors

→ Quarantine record

→ Do not write the record to D1