create table anniversary (
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
