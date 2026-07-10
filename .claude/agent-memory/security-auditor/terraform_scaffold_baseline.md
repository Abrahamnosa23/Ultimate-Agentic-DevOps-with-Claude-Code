---
name: terraform-scaffold-baseline
description: Baseline security posture of terraform/ (S3+CloudFront static site) as of first audit 2026-07-10
metadata:
  type: project
---

The `terraform/` directory (providers.tf, variables.tf, main.tf, outputs.tf, backend.tf) provisions a
private S3 bucket + CloudFront distribution to host the static portfolio site (see root CLAUDE.md — the
site itself is plain HTML/CSS with no build step; the Terraform is purely for optional AWS hosting).

Baseline strengths already implemented correctly (verified 2026-07-10, main.tf):
- S3 public access block has all four flags true, bucket ownership controls = BucketOwnerEnforced (no ACLs).
- CloudFront uses OAC (`aws_cloudfront_origin_access_control`), not legacy OAI.
- Bucket policy scoped to the specific distribution via `AWS:SourceArn` condition, and
  `aws_s3_bucket_policy` has `depends_on` the public access block (avoids PAB/policy race).
- `viewer_protocol_policy = "redirect-to-https"` satisfies HTTP->HTTPS redirect requirement.
- No hardcoded account ID/ARNs — account id comes from `data.aws_caller_identity.current`.

Recurring gaps found on first audit (still open as of 2026-07-10, none are Critical):
- No `aws_s3_bucket_server_side_encryption_configuration` for the site bucket (no encryption at rest).
- No `aws_s3_bucket_versioning` on the site bucket.
- No S3 access logging and no CloudFront `logging_config` block — no audit trail.
- No `aws_cloudfront_response_headers_policy` — missing CSP/X-Frame-Options/HSTS (High severity, explicit
  checklist item).
- `viewer_certificate` only sets `cloudfront_default_certificate = true` with no `minimum_protocol_version`;
  if `var.domain_name` is ever set this is actually broken (custom aliases require an ACM cert + SNI), so a
  domain_name change would need a paired `acm_certificate_arn` variable and `minimum_protocol_version =
  "TLSv1.2_2021"`.
- No WAFv2 Web ACL associated with the distribution.
- `backend.tf` defaults to local state (S3 backend block commented out) — no state encryption/versioning/
  locking enforced by default; the bootstrap bucket described in the comment is never defined as actual
  Terraform code with its own encryption/versioning/public-access-block.

**Why this matters:** these are consistent, structural gaps rather than one-off mistakes — if re-auditing
this repo later, check first whether these specific gaps have been closed rather than re-deriving the whole
list from scratch.

**How to apply:** on future audits of `terraform/`, diff the current file contents against this list; only
report gaps that are still present, and note explicitly in the report which of these have since been fixed.

Related: [[gitignore-is-a-directory]].
