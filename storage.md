# Postgres Backup Storage Plan

## Goal
Create an automated, low-cost backup flow for Postgres with:
- local offline copy (external hard drive)
- encrypted cloud copies in multiple providers
- defined retention and restore testing

## Scope
- Backup source: production Postgres via `DATABASE_URL`
- Backup format: custom pg dump (`pg_dump -Fc`)
- Encryption: required before any cloud upload
- Destinations:
  - external hard drive (local)
  - cloud provider #1 (via `rclone`)
  - cloud provider #2 (optional, via `rclone`)

## Backup Strategy
1. Run nightly full backup with `pg_dump`.
2. Encrypt backup file.
3. Copy encrypted file to:
   - local external drive
   - cloud remote 1
   - cloud remote 2 (if configured)
4. Apply retention cleanup.
5. Log success/fail status.

## Suggested Commands

### 1) Generate backup
```bash
pg_dump "$DATABASE_URL" -Fc -f "backups/$(date +%F_%H%M).dump"
```

### 2) Encrypt backup (example with `age`)
```bash
age -r "$AGE_PUBLIC_KEY" -o "backups/$(date +%F_%H%M).dump.age" "backups/$(date +%F_%H%M).dump"
```

### 3) Copy to external hard drive
```bash
rsync -av --delete backups/ "/Volumes/ExternalDrive/db-backups/"
```

### 4) Copy to cloud remotes (`rclone`)
```bash
rclone copy backups/ remote1:db-backups
rclone copy backups/ remote2:db-backups
```

### 5) Retention cleanup (example policy)
- Keep daily backups: 14
- Keep weekly backups: 8
- Keep monthly backups: 12

Implement with a cleanup script that deletes expired files across local and remotes.

## Automation
- Schedule via `cron` (or GitHub Actions / CI runner if preferred).
- Recommended schedule: nightly off-peak (for example, `2:00 AM` local time).
- Send alert on failure (email/Slack/webhook).

## Security Requirements
- Never store plaintext dumps in cloud.
- Keep encryption private key outside git and outside shared notebooks.
- Restrict backup destination access to least privilege.
- Use dedicated credentials for each cloud remote.

## Restore Validation
- Monthly restore drill to a non-production database.
- Verify:
  - database can be restored
  - key tables exist
  - row counts are reasonable
  - app can query restored data

Example:
```bash
pg_restore -d "$TEST_DATABASE_URL" latest.dump
```

## Implementation Checklist
- [ ] Choose encryption tool (`age` or `gpg`)
- [ ] Create backup script (`scripts/backup_postgres.sh`)
- [ ] Configure `rclone` remotes
- [ ] Configure external drive path
- [ ] Add retention cleanup script
- [ ] Add cron entry
- [ ] Add alerting on failure
- [ ] Run first backup manually
- [ ] Run first restore test

## Notes
- “Free” cloud storage tiers are limited; expect paid usage as data grows.
- Multi-destination redundancy is more important than maximizing free tier.
