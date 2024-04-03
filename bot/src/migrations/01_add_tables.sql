create schema tgbot;

set search_path to tgbot;

create type language_t_v1 as enum (
    'ru', 'en'
    );

create type level_t_v1 as enum (
    'A1', 'A2', 'A3'
    );

create table users (
    user_id smallserial primary key,
    tg_login text not null,
    login varchar(16) not null unique,
    password varchar(16) not null,
    words_in_lesson smallint not null,
    native_language language_t_v1  not null,
    language_to_learn language_t_v1 not null
);

create table words (
    word_id serial,
    language language_t_v1,
    level level_t_v1 not null,
    word text not null,
    primary key (word_id, language)
);

create table words_in_progress (
    user_id smallserial,
    word_id serial,
    language language_t_v1 not null,
    number_of_repetitions smallint not null,
    primary key (user_id, word_id, language),
    foreign key (user_id) references Users (user_id),
    foreign key (word_id, language) references Words (word_id, language)
);