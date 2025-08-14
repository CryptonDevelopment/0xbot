-- upgrade --
ALTER TABLE "timer_message" ADD "start" BIGINT NOT NULL  DEFAULT 1754691072;
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754691072;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754690659;
ALTER TABLE "timer_message" DROP COLUMN "start";
