CREATE TABLE anniversary (
    aid integer primary key autoincrement,
    aname text not null,
    adate text not null,
    is_holiday int not null, 
    uid text not null
);

CREATE TABLE schedule (
    sid integer primary key autoincrement,
    uid text not null,
    sdate text not null,
    title text not null,
    place text,
    start_time text,
    end_time text,
    is_important int default 0,
    memo text
);

CREATE TABLE user (
    uid text primary key,
    pwd text not null,
    uname text not null,
    email text not null
);

CREATE TABLE profile (
    email text primary key,
    image text,
    stateMsg text,
    github text,
    insta text,
    addr text
);
