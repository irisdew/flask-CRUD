create table if not exists user(
    id int not null AUTO_INCREMENT,
    fullname varchar(32) not null,
    email varchar(64) not null,
    password varchar(128) not null,
    primary key(id),
    unique(email)
);

create table if not exists board(
    id int not null AUTO_INCREMENT,
    name varchar(64) not null,
    content varchar(100) not null.
    create_date timestamp default NOW(),
    primary key (id)
);

create table if not exists boardArticle(
    id int not null AUTO_INCREMENT,
    title varchar(64) not null,
    content text,
    board_id int not null,
    create_date timestamp default NOW(),
    primary key (id),
    foreign key (board_id) references board(id)
);