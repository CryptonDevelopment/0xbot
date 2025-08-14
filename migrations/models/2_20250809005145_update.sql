-- upgrade --
CREATE TABLE IF NOT EXISTS "message_to_delete" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "message_id" BIGINT NOT NULL
);;
CREATE TABLE IF NOT EXISTS "timer_message" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "message_id" BIGINT NOT NULL,
    "timer" BIGINT NOT NULL,
    "after" TEXT NOT NULL
);;
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754689905;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "last_seen" SET DEFAULT 1754672757;
DROP TABLE IF EXISTS "message_to_delete";
DROP TABLE IF EXISTS "timer_message";
