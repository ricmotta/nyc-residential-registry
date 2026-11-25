#!/bin/sh
# Writes the S3 identity from environment variables, then starts a single-node SeaweedFS
# (master, volume, filer and S3 gateway on port 8333).
set -eu

cat > /tmp/s3.json <<JSON
{
  "identities": [
    {
      "name": "registry",
      "credentials": [{"accessKey": "${S3_ACCESS_KEY}", "secretKey": "${S3_SECRET_KEY}"}],
      "actions": ["Admin", "Read", "List", "Tagging", "Write"]
    }
  ]
}
JSON

exec weed server -dir=/data -s3 -s3.port=8333 -s3.config=/tmp/s3.json
