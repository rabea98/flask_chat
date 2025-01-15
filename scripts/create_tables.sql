create table chat_messages(
	id int not null auto_increment primary key,
	date datetime not null,
	room varchar(255) not null,
	username varchar(255) not null,
	message varchar(255) not null
);