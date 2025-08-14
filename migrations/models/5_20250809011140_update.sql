-- upgrade --
ALTER TABLE "timer_message" ADD "created" BIGINT NOT NULL  DEFAULT 1754691100;
ALTER TABLE "timer_message" DROP COLUMN "start";
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754691100;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754691074;
ALTER TABLE "timer_message" ADD "start" BIGINT NOT NULL  DEFAULT 1754691074;
ALTER TABLE "timer_message" DROP COLUMN "created";
