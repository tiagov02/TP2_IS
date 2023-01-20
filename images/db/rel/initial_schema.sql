CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

create table if not exists teams
(
    id         uuid      default uuid_generate_v4() not null
        primary key,
    name       varchar(250)                         not null,
    created_on timestamp default now()              not null,
    updated_on timestamp default now()              not null
);

alter table teams
    owner to is;

create table if not exists countries
(
    id         uuid      default uuid_generate_v4() not null
        primary key,
    name       varchar(250)                         not null
        unique,
    geom       geometry,
    created_on timestamp default now()              not null,
    updated_on timestamp default now()              not null
);

alter table countries
    owner to is;

create table if not exists players
(
    id         uuid      default uuid_generate_v4() not null
        primary key,
    name       varchar(250)                         not null,
    age        integer                              not null,
    team_id    uuid
        constraint players_teams_id_fk
            references teams
            on delete set null,
    country_id uuid                                 not null
        constraint players_countries_id_fk
            references countries
            on delete cascade,
    created_on timestamp default now()              not null,
    updated_on timestamp default now()              not null
);

alter table players
    owner to is;

create table if not exists suicides
(
    id             uuid      default uuid_generate_v4() not null
        constraint suicides_pk
            primary key,
    min_age        integer,
    max_age        integer,
    tax            double precision,
    population_no  integer,
    suicides_no    integer,
    generation     varchar(100),
    gdp_for_year   varchar(100),
    hdi_for_year   double precision,
    gdp_per_capita double precision,
    year           integer,
    id_country     uuid                                 not null
        constraint suicides_countries_id_fk
            references countries,
    created_on     timestamp default now(),
    updated_on     timestamp default now(),
    sex            varchar(100)
);

alter table suicides
    owner to is;




