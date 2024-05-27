do $$
begin
    if not exists (
        select 1 from pg_type 
        where typname = 'language_t_v1') then
        create type language_t_v1 as enum (
            'ru', 'en');
    end if;
end
$$;

do $$
begin
    if not exists (
        select 1 from pg_type 
        where typname = 'level_t_v1') then
        create type level_t_v1 as enum (
            'A1', 'A2', 'A3');
    end if;
end
$$;

create table if not exists users (
    user_id smallserial primary key,
    tg_login text,
    login varchar(50) not null unique,
    password varchar(50) not null,
    words_in_lesson smallint not null,
    native_language language_t_v1  not null,
    language_to_learn language_t_v1 not null,
    word_level level_t_v1 not null
);

create table if not exists words (
    word_id integer,
    language language_t_v1,
    level level_t_v1 not null,
    word text not null,
    primary key (word_id, language)
);

create table if not exists words_in_progress (
    user_id integer,
    word_id integer,
    language language_t_v1,
    number_of_repetitions smallint not null,
    primary key (user_id, word_id, language),
    foreign key (user_id) references Users (user_id),
    foreign key (word_id, language) references Words (word_id, language)
);

create extension if not exists plpgsql with schema public;
create extension if not exists pg_trgm with schema public;
create index if not exists word_trgm_index on words using GIN (word gin_trgm_ops);
create index if not exists user_tg_login_index on users (tg_login);
create index if not exists user_login_index on users (login);

insert into words (word_id, language, level, word) values (51, 'en', 'A2', 'achievement');
insert into words (word_id, language, level, word) values (51, 'ru', 'A2', 'достижение');
insert into words (word_id, language, level, word) values (52, 'en', 'A3', 'acid');
insert into words (word_id, language, level, word) values (52, 'ru', 'A3', 'кислота');
insert into words (word_id, language, level, word) values (53, 'en', 'A1', 'acknowledge');
insert into words (word_id, language, level, word) values (53, 'ru', 'A1', 'сознавать');
insert into words (word_id, language, level, word) values (54, 'en', 'A1', 'acquire');
insert into words (word_id, language, level, word) values (54, 'ru', 'A1', 'приобретать');
insert into words (word_id, language, level, word) values (55, 'en', 'A3', 'acquisition');
insert into words (word_id, language, level, word) values (55, 'ru', 'A3', 'приобретение');
insert into words (word_id, language, level, word) values (56, 'en', 'A3', 'acre');
insert into words (word_id, language, level, word) values (56, 'ru', 'A3', 'акра');
insert into words (word_id, language, level, word) values (57, 'en', 'A1', 'across');
insert into words (word_id, language, level, word) values (57, 'ru', 'A1', 'через');
insert into words (word_id, language, level, word) values (58, 'en', 'A2', 'act');
insert into words (word_id, language, level, word) values (58, 'ru', 'A2', 'действовать');
insert into words (word_id, language, level, word) values (59, 'en', 'A1', 'action');
insert into words (word_id, language, level, word) values (59, 'ru', 'A1', 'действие');
insert into words (word_id, language, level, word) values (60, 'en', 'A1', 'activate');
insert into words (word_id, language, level, word) values (60, 'ru', 'A1', 'активировать');
insert into words (word_id, language, level, word) values (61, 'en', 'A3', 'activation');
insert into words (word_id, language, level, word) values (61, 'ru', 'A3', 'активация');
insert into words (word_id, language, level, word) values (62, 'en', 'A1', 'active');
insert into words (word_id, language, level, word) values (62, 'ru', 'A1', 'активный');
insert into words (word_id, language, level, word) values (63, 'en', 'A3', 'activist');
insert into words (word_id, language, level, word) values (63, 'ru', 'A3', 'активист');
insert into words (word_id, language, level, word) values (64, 'en', 'A1', 'activity');
insert into words (word_id, language, level, word) values (64, 'ru', 'A1', 'активность');