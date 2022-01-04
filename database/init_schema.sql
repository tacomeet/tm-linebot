CREATE TYPE "user_status" AS ENUM (
  'none',
  'bn_create',
  'bn_create_trackl',
  'bn_create_track2',
  'bn_create_track3',
  'bn_create_track4',
  'self_ref',
  'catch_rec',
  'contact'
);

-- CREATE TABLE "users" (
--   "id" int PRIMARY KEY,
--   "name" varchar NOT NULL,
--   "status" user_status NOT NULL,
--   "thread_ts" varchar,
--   "follow" bool NOT NULL,
--   "created_at" timestamp NOT NULL DEFAULT (now())
-- );

CREATE TABLE "threads" (
  "ts" varchar PRIMARY KEY,
  "user_id" int NOT NULL
);
