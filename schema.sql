create table if not exists game (
    game_id serial unique primary key,
    title varchar(255) not null,
    publisher varchar(255), 
    description varchar(255), 
    developer varchar(255),
    thumbnail_link varchar(255),
    release_date date
);

create table if not exists user_data (
    user_id serial unique primary key,
    username varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null,
    first_name varchar(255)
);

create table if not exists review (
    review_id serial unique primary key,
    review_date date not null, 
    rating_score integer not null, 
    replayability_score integer, 
    graphics_score integer,
    description varchar(255) not null
);

create table if not exists tag (
    tag_id serial unique primary key,
    tag_description varchar(255) not null
);

create table if not exists game_review (
    review_id serial unique,
    game_id serial unique,
    constraint review_id_fk foreign key (review_id) references review(review_id) 
    on update cascade on delete cascade,
    constraint game_id_fk foreign key (game_id) references game(game_id)
    on update cascade on delete cascade, 
    primary key (game_id, review_id)
);

create table if not exists user_favorite (
    user_id serial unique,
    game_id serial unique,
    constraint user_id_fk foreign key (user_id) references user_data(user_id) 
    on update cascade on delete cascade,
    constraint game_id_fk foreign key (game_id) references game(game_id)
    on update cascade on delete cascade, 
    primary key (game_id, user_id)
);

create table if not exists tag_game (
    tag_id serial unique,
    game_id serial unique,
    constraint tag_id_fk foreign key (tag_id) references tag(tag_id) 
    on update cascade on delete cascade,
    constraint game_id_fk foreign key (game_id) references game(game_id)
    on update cascade on delete cascade, 
    primary key (game_id, tag_id)
);