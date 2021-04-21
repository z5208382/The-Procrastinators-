create domain ShortString as varchar(16);
create domain MediumString as varchar(64);
create domain LongString as varchar(256);
create domain TextString as varchar(16384);
create domain ShortName as varchar(16);
create domain MediumName as varchar(64);
create domain LongName as varchar(128);

create table Societies (
    id              TextString, 
    uni             LongString, 
    name            LongString, 
    description     TextString, 
    societyImage    TextString,
    primary key (id)
);

create table Categories (
    id          serial, 
    type        LongString,
    primary key (id)
);

create table Universities ( 
    id          integer, 
    name        LongName,
    primary key (id)
);

create table Events (
	id          BIGINT,
	eventTitle  TextString,
    startDate   LongString, -- change to date once its working 
    endDate     LongString, -- change to date once its working
    --startTime   LongString,
    --endTime     LongString, 
    description TextString, 
    location    TextString, 
    host        TextString references Societies(id), 
    eventImage  LongString, 
    primary key (id)
);

create table EventCategories (
    eventId     integer references Events(id),
    categoryId  integer references Categories(id),
    primary key (eventId, categoryId)
);

create table Profiles (
    id              integer, 
    fName           LongName, 
    lName           LongName,
    uni             integer references Universities(id),  
    faveSoc         TextString references Societies(id), 
    prevAttended    integer references Events(id), 
    primary key (id)
);
