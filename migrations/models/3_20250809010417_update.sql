-- upgrade --
ALTER TABLE "timer_message" ADD "user_id" BIGINT NOT NULL;
ALTER TABLE "timer_message" DROP COLUMN "message_id";
ALTER TABLE "timer_message" DROP COLUMN "chat_id";
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754690657;
ALTER TABLE "timer_message" ADD CONSTRAINT "fk_timer_me_user_0b189f9a" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "timer_message" DROP CONSTRAINT "fk_timer_me_user_0b189f9a";
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754689907;
ALTER TABLE "timer_message" ADD "message_id" BIGINT NOT NULL;
ALTER TABLE "timer_message" ADD "chat_id" BIGINT NOT NULL;
ALTER TABLE "timer_message" DROP COLUMN "user_id";
