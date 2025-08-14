-- upgrade --
ALTER TABLE "timer_message" ADD "active" BOOL NOT NULL  DEFAULT True;
ALTER TABLE "timer_message" ALTER COLUMN "created" SET DEFAULT 1754693545;
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754693545;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754691102;
ALTER TABLE "timer_message" DROP COLUMN "active";
ALTER TABLE "timer_message" ALTER COLUMN "created" SET DEFAULT 1754691102;
