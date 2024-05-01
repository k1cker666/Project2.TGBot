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
    tg_login text not null,
    login varchar(16) not null unique,
    password varchar(16) not null,
    words_in_lesson smallint not null,
    native_language language_t_v1  not null,
    language_to_learn language_t_v1 not null,
    level level_t_v1 not null
);

create table if not exists words (
    word_id int,
    language language_t_v1,
    level level_t_v1 not null,
    word text not null,
    primary key (word_id, language)
);

create table if not exists words_in_progress (
    user_id smallserial,
    word_id int,
    language language_t_v1 not null,
    number_of_repetitions smallint not null,
    primary key (user_id, word_id, language),
    foreign key (user_id) references Users (user_id),
    foreign key (word_id, language) references Words (word_id, language)
);

create extension if not exists plpgsql with schema public;
create extension if not exists pg_trgm with schema public;
create index if not exists word_trgm_index on words using GIN (word gin_trgm_ops);
create unique index if not exists user_tg_login on users (tg_login);