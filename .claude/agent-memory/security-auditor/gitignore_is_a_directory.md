---
name: gitignore-is-a-directory
description: Repo root .gitignore is a directory, not a file — Git is not actually ignoring anything
metadata:
  type: project
---

At the repo root, `.gitignore` is a **directory** (containing subfolders like `.gitignore/terraform` and
`.gitignore/.terraform`), not a file. Confirmed 2026-07-10 via `git status` output (`D .gitignore/.terraform`,
`?? .gitignore/terraform`) and by `Read` erroring with `EISDIR` when attempting to read it as a file.

**Why this matters:** because there is no real `.gitignore` file, Git applies no ignore rules at all. This is
directly relevant to Terraform security reviews: `terraform/.terraform/` (provider binaries, currently
present) and any future `terraform.tfstate` / `*.tfvars` files are not excluded from version control. A local
Terraform state file can contain the real AWS account ID and resource ARNs, so committing it would leak data
that the security checklist explicitly says must not be hardcoded/checked in.

**How to apply:** flag this in every Terraform/security audit of this repo until it is fixed (delete the
`.gitignore` directory and replace it with a real file containing at least `.terraform/`,
`.terraform.lock.hcl`, `*.tfstate`, `*.tfstate.*`, `*.tfvars`, `crash.log`). Do not assume it has been fixed
just because a prior report flagged it — re-verify by trying to Read `.gitignore` as a file each time.

Related: [[terraform-scaffold-baseline]].
