-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/lm5ZNw
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "user_id"  SERIAL  NOT NULL,
    "username" string   NOT NULL,
    "password" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "user_id"
     ),
    CONSTRAINT "uc_User_username" UNIQUE (
        "username"
    )
);

CREATE TABLE "Favs" (
    "fav_id"  SERIAL  NOT NULL,
    "fav_name" string   NOT NULL,
    "fav_link" string   NOT NULL,
    CONSTRAINT "pk_Favs" PRIMARY KEY (
        "fav_id"
     )
);

CREATE TABLE "Drinks" (
    "drink_id"  SERIAL  NOT NULL,
    "drink_name" string   NOT NULL,
    "recipe" string   NOT NULL,
    "ingredient1" string   NOT NULL,
    "ingredient2" string   NULL,
    "ingredient3" string   NULL,
    "ingredient4" string   NULL,
    "ingredient5" string   NULL,
    "ingredient6" string   NULL,
    "ingredient7" string   NULL,
    "ingredient8" string   NULL,
    "ingredient9" string   NULL,
    "ingredient10" string   NULL,
    "ingredient11" string   NULL,
    "ingredient12" string   NULL,
    "ingredient13" string   NULL,
    "ingredient14" string   NULL,
    "ingredient15" string   NULL,
    CONSTRAINT "pk_Drinks" PRIMARY KEY (
        "drink_id"
     )
);

ALTER TABLE "User" ADD CONSTRAINT "fk_User_user_id" FOREIGN KEY("user_id")
REFERENCES "Favs" ("fav_id");

ALTER TABLE "Favs" ADD CONSTRAINT "fk_Favs_fav_name" FOREIGN KEY("fav_name")
REFERENCES "Drinks" ("drink_name");

