# HabotConnect — Junior Cloud & DevOps Engineer Hiring Project

## Candidate

**Name:** Parth Rawat
**Role:** Junior Cloud & DevOps Engineer (GCP / Django / React)

---

## 1. Project Overview

This repository contains the implementation for the HabotConnect Junior Cloud & DevOps Engineer hiring project.

The solution focuses on:

- Secure Infrastructure as Code using Terraform
- Secure and fail-closed CI/CD automation
- Deterministic student onboarding validation
- DCYN (Yes/No) decision logic
- Django REST Framework serializer validation
- D0 raw-data landing and D1 validated-data processing
- Quarantine of invalid records
- BigQuery Row-Level Security
- Automated testing

The design follows the assessment requirements around security, least privilege, data integrity, mistake-proofing (Poka-Yoke), and structural discipline.

---

## 2. Architecture

The implementation follows this logical flow:

```text
D0 Raw Landing
        |
        v
Incoming Student JSON
        |
        v
DCYN / Validation Gate
        |
   +----+----+
   |         |
 VALID     INVALID
   |         |
   v         v
D1 Staged   Quarantine
& Enforced
   |
   v
BigQuery with Row-Level Security
```

The D0 layer represents the raw landing area. The D1 layer contains only validated records that have passed the deterministic validation rules.

---

## 3. Repository Structure

```text
habotconnect-junior-cloud-devops/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   ├── storage.tf
│   ├── iam.tf
│   ├── bigquery.tf
│   └── .terraform.lock.hcl
│
├── student_onboarding/
│   ├── __init__.py
│   ├── requirements.txt
│   ├── models.py
│   ├── serializers.py
│   └── validators.py
│
├── schema/
│   ├── schema_mapping.md
│   ├── student_onboarding.json
│   └── student_onboarding_batch.json
│
├── pipeline/
│   ├── __init__.py
│   └── process_onboarding.py
│
├── tests/
│   ├── __init__.py
│   ├── demo_validation_failures.py
│   ├── test_pipeline.py
│   ├── test_serializers.py
│   └── test_validators.py
│
├── docs/
├── presentation/
├── screenshots/
├── .gitignore
├── .yamllint.yml
├── README.md
└── requirements.txt
```

---

## 4. Task 1 — Secure GCP Infrastructure

Terraform is used to define the D0 and D1 infrastructure.

### D0 — Raw Landing

The D0 layer uses a Google Cloud Storage bucket with:

- Uniform bucket-level access
- Public access prevention
- Object versioning
- Staging/environment labels
- Terraform-managed configuration

The bucket is intended to receive raw onboarding objects.

### Least-Privilege Ingestion

A dedicated service account is created for D0 ingestion.

The service account receives:

- `roles/storage.objectCreator`

with an IAM condition restricting object creation to the:

- `raw/` prefix

This prevents the ingestion identity from receiving unnecessary broader storage permissions.

### D1 — Staged and Enforced

Terraform creates the:

- `d1_staged_enforced` BigQuery dataset
- `student_onboarding_staged` table

The table contains validated onboarding fields and an:

- `access_scope` field

used by the Row-Level Security policy.

### BigQuery Row-Level Security

A BigQuery Row-Level Security policy restricts the analytics service account to records where:

- `access_scope = 'ANALYTICS'`

The analytics identity receives:

- `roles/bigquery.dataViewer`

at the dataset level.

The combination of dataset-level access and row-level filtering provides additional protection against unintended access to rows outside the analytics scope.

---

## 5. Task 2 — Fail-Closed CI/CD

The GitHub Actions workflow is implemented in:

- `.github/workflows/ci.yml`

The security gate runs automatically for pushes and pull requests targeting the `main` and `develop` branches.

### Security and Quality Checks

The pipeline performs:

- Terraform formatting validation
- Terraform initialization
- Terraform validation
- YAML linting
- Hardcoded-secret scanning using Gitleaks
- Required project structure verification
- Python dependency installation
- Python compilation checks
- Automated validation tests

### Fail-Closed Behaviour

The workflow is intentionally designed so that a failed security or quality check causes the job to fail.

For example, if a hardcoded secret is detected by Gitleaks, the security gate fails and the pull request cannot be merged when the required GitHub branch protection checks are not passing.

A fake-secret test was used to demonstrate this behaviour.

The resulting workflow demonstrated:

- Security Gate: FAILED
- Python Validation: PASSED
- Merge: BLOCKED

After removing the test secret, the clean repository passed the security gate.

---

## 6. Task 3 — Deterministic Student Onboarding

The onboarding implementation is contained in:

- `student_onboarding/`
- `pipeline/process_onboarding.py`

The validation layer uses Django REST Framework serializers.

The objective is to eliminate manual interpretation of onboarding data.

### Proposed Input Schema

The assessment brief does not provide a concrete student JSON payload or field-level validation limits.

Therefore, the schema and validation limits implemented in this repository are explicitly proposed engineering rules rather than requirements claimed to have been supplied by HabotConnect.

The proposed fields are:

| Field | Type | Validation |
|---|---|---|
| student_name | string | 2–100 characters |
| email | string | Valid email, maximum 254 characters |
| phone | string | Exactly 10 digits |
| age | integer | 18–60 |
| has_passport | boolean | true/false only |
| has_academic_documents | boolean | true/false only |
| english_proficiency | boolean | true/false only |
| willing_to_relocate | boolean | true/false only |
| has_relevant_experience | boolean | true/false only |

---

## 7. DCYN Logic

The onboarding process uses deterministic Yes/No decision gates.

### DCYN-1 — Required Information

All mandatory fields must be present.

- YES → Continue
- NO → Reject and quarantine

### DCYN-2 — Data Type

All fields must use the expected data type.

- YES → Continue
- NO → Reject and quarantine

### DCYN-3 — Field Validation

All values must satisfy their defined validation constraints.

- YES → Continue
- NO → Reject and quarantine

### DCYN-4 — Binary Decision

DCYN fields must contain actual boolean values.

- `true` → YES
- `false` → NO

Values such as:

- `"yes"`
- `"no"`
- `"true"`
- `"false"`

are rejected.

### DCYN-5 — Final Onboarding Decision

Mandatory onboarding conditions are evaluated deterministically.

- Valid records continue to D1.
- Invalid records are rejected and quarantined.

---

## 8. Poka-Yoke / Mistake-Proofing

The implementation rejects:

- Missing required fields
- Unexpected fields
- Incorrect data types
- Invalid email addresses
- Invalid phone numbers
- Ages outside the defined range
- Strings outside defined length limits
- Non-boolean DCYN values

The system therefore does not depend on a human operator interpreting ambiguous input.

---

## 9. Data Processing Pipeline

The local processing pipeline reads the raw onboarding batch and processes each record through the Django REST Framework serializer.

- Valid records are written to the D1 output.
- Invalid records are written to the quarantine output.

The D1 records receive:

- `access_scope = ANALYTICS`

to align the local processing output with the BigQuery Row-Level Security design.

---

## 10. Demonstration Results

The test batch contains:

- Total records: 10
- Accepted: 6
- Rejected: 4
- D1 records: 6
- Quarantined: 4

The rejected records include examples of:

- Invalid age
- Invalid phone number
- Failed mandatory passport decision
- Unexpected field

No rejected record is written to the D1 output.

---

## 11. Automated Testing

The repository contains unit tests for:

- Serializer validation
- Individual validators
- Batch processing
- Acceptance/rejection behaviour
- Quarantine behaviour
- D1 output generation
- D1 access scope

Latest local test result:

- Ran 15 tests
- OK

The same Python test suite is executed by GitHub Actions.

---

## 12. Terraform Validation

The Terraform configuration was locally validated using:

```bash
terraform fmt
terraform validate
terraform plan
```

The final Terraform plan successfully evaluated the infrastructure design with:

- Plan: 8 to add, 0 to change, 0 to destroy

No Terraform state or plan files are committed to the repository.

---

## 13. GCP Deployment Limitation

The Terraform configuration was validated and planned successfully.

An actual GCP resource deployment could not be completed in the available assessment project because the associated Google Cloud billing account was inactive.

Therefore, this repository does not claim that the GCP resources were successfully deployed to the cloud.

The implementation should be applied to an active-billing GCP project using:

```bash
terraform apply
```

after the required project permissions and billing configuration are available.

---

## 14. Security Principles

The implementation applies the following principles:

- Least privilege
- Fail-closed CI/CD
- Public access prevention
- Uniform bucket-level access
- IAM conditions
- Row-Level Security
- Strict schema validation
- Deterministic binary decisions
- Invalid-record quarantine
- Automated testing
- Infrastructure as Code
- No committed Terraform state
- No committed hardcoded secrets

---

## 15. Reproduction

### Terraform

```bash
cd terraform

terraform init
terraform fmt -check -recursive
terraform validate
terraform plan
```

To deploy against a different project:

```bash
terraform plan -var="project_id=YOUR_PROJECT_ID"
```

and, after confirming the plan:

```bash
terraform apply -var="project_id=YOUR_PROJECT_ID"
```

After testing a temporary deployment:

```bash
terraform destroy -var="project_id=YOUR_PROJECT_ID"
```

### Python Tests

Install dependencies:

```bash
pip install -r student_onboarding/requirements.txt
```

Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Local Pipeline

The local pipeline processes the D0 raw input and generates:

- `pipeline/output/d1_valid_records.json`
- `pipeline/output/quarantine_records.json`

Generated output and local raw-data files are excluded from Git using `.gitignore`.

---

## 16. Conclusion

This implementation provides a secure and deterministic foundation for the requested cloud and DevOps workflow.

Terraform defines the security-focused GCP infrastructure, GitHub Actions provides a fail-closed automation gate, and Django REST Framework provides strict deterministic validation for student onboarding data.

The local implementation and automated tests have been completed and validated. Actual cloud deployment remains dependent on an active GCP billing configuration.