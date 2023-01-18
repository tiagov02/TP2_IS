create table if not exists converted_documents
(
    id         serial
        primary key,
    src        varchar(250)            not null
        unique,
    file_size  bigint                  not null,
    dst        varchar(250)            not null
        unique,
    created_on timestamp default now() not null,
    updated_on timestamp default now() not null
);

alter table converted_documents
    owner to is;

create table if not exists imported_documents
(
    id         serial
        primary key,
    file_name  varchar(250)            not null
        unique,
    xml        xml                     not null,
    created_on timestamp default now() not null,
    updated_on timestamp default now() not null,
    estado     varchar(100)
);

alter table imported_documents
    owner to is;


