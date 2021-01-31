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

create table if not exists user(
    id int not null AUTO_INCREMENT,
    fullname varchar(32) not null,
    email varchar(64) not null,
    password varchar(128) not null,
    primary key(id),
    unique(email)
);


INSERT INTO board (name) VALUES ('test1');
INSERT INTO boardArticle (title, content, board_id) VALUES ('제목1', '내용1', 1);
INSERT INTO boardArticle (title, content, board_id) VALUES ('제목2', '내용2', 1);
INSERT INTO boardArticle (title, content, board_id) VALUES ('제목3', '내용3', 1);