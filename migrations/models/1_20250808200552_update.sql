-- upgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754672752;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754672748;
