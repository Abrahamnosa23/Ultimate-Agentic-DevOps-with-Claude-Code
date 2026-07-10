# ---------------------------------------------------------------------------
# Remote state backend (S3)
# ---------------------------------------------------------------------------
# By default this configuration uses LOCAL state so you can bootstrap without
# a pre-existing state bucket.
#
# To migrate to an S3 remote backend:
#
#   1. First run WITHOUT the backend block below (local state):
#        terraform init
#        terraform apply
#      This creates the site resources. Separately, create a dedicated S3
#      bucket (and optionally a DynamoDB table for locking) to hold state,
#      e.g. `portfolio-site-tfstate` with versioning enabled.
#
#   2. Uncomment the `backend "s3"` block below and set the bucket name.
#
#   3. Migrate your existing local state into the bucket:
#        terraform init -migrate-state
#
# ---------------------------------------------------------------------------

# terraform {
#   backend "s3" {
#     bucket         = "portfolio-site-tfstate"   # must already exist
#     key            = "portfolio-site/terraform.tfstate"
#     region         = "ap-south-1"
#     encrypt        = true
#     dynamodb_table = "portfolio-site-tflock"    # optional: state locking
#   }
# }
