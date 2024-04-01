# parent ( 부모유저 )
# +---------------+--------------+------+-----+---------+-------+
# | Field         | Type         | Null | Key | Default | Extra |
# +---------------+--------------+------+-----+---------+-------+
# | parent_id     | varchar(255) | NO   | PRI | NULL    |       |
# | password      | varchar(255) | YES  |     | NULL    |       |
# | email         | varchar(255) | NO   |     | NULL    |       |
# | name          | varchar(50)  | YES  |     | NULL    |       |
# | nickname      | varchar(255) | NO   |     | NULL    |       |
# | signInMethod  | varchar(50)  | YES  |     | NULL    |       |
# | emailVerified | tinyint(1)   | YES  |     | NULL    |       |
# | photoId       | varchar(255) | YES  |     | NULL    |       |
# | description   | varchar(255) | YES  |     | NULL    |       |
# +---------------+--------------+------+-----+---------+-------+
# CREATE TABLE parent (
#     parent_id VARCHAR(255) PRIMARY KEY NOT NULL,
#     password VARCHAR(255),
#     email VARCHAR(255) NOT NULL,
#     name VARCHAR(50),
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50),
#     emailVerified VARCHAR(255),
#     photoId VARCHAR(255),
#     description VARCHAR(255)
# );


# baby ( 아기 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | baby_id   | varchar(255) | NO   | PRI | NULL    |       |
# | name      | varchar(255) | NO   |     | NULL    |       |
# | gender    | varchar(50)  | NO   |     | NULL    |       |
# | birthDate | datetime     | YES  |     | NULL    |       |
# | bloodType | char(3)      | YES  |     | NULL    |       |
# | photoId   | varchar(255) | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE baby (
#     baby_id VARCHAR(255) NOT NULL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     gender VARCHAR(50) NOT NULL,
#     birthDate DATETIME,
#     bloodType CHAR(3),
#     photoId VARCHAR(255)
# );


# ppconnect ( 유저와 유저 연결 )
# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | ppc_id     | int(11)      | NO   | PRI | NULL    |       |
# | parent_id1 | varchar(255) | NO   | MUL | NULL    |       |
# | parent_id2 | varchar(255) | NO   | MUL | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# CREATE TABLE ppconnect (
#     ppc_id INT PRIMARY KEY NOT NULL,
#     parent_id1 VARCHAR(255) NOT NULL,
#     parent_id2 VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id1) REFERENCES parent(parent_id),
#     FOREIGN KEY (parent_id2) REFERENCES parent(parent_id)
# );


# pbconnect (유저와 아기 연결 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | pbc_id    | int(11)      | NO   | PRI | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE pbconnect (
#     pbc_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );


# pcconnect ( 유저 채팅 연결 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | pcc_id    | int(11)      | NO   | PRI | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | room_id   | int(11)      | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE pcconnect (
#     pcc_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     room_id INT NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (room_id) REFERENCES chat(room_id)
# );


# post ( 게시물 )
# +-------------+------------------+------+-----+---------+-------+
# | Field       | Type             | Null | Key | Default | Extra |
# +-------------+------------------+------+-----+---------+-------+
# | post_id     | int(11)          | NO   | PRI | NULL    |       |
# | parent_id   | varchar(255)     | NO   |     | NULL    |       |
# | post        | text             | NO   |     | NULL    |       |
# | photos      | text             | YES  |     | NULL    |       |
# | post_time   | datetime         | NO   |     | NULL    |       |
# | modify_time | datetime         | YES  |     | NULL    |       |
# | delete_time | datetime         | YES  |     | NULL    |       |
# | heart       | int(10) unsigned | YES  |     | NULL    |       |
# | share       | int(10) unsigned | YES  |     | NULL    |       |
# | script      | int(10) unsigned | YES  |     | NULL    |       |
# | comment     | int(10) unsigned | YES  |     | NULL    |       |
# | hash        | varchar(100)     | YES  |     | NULL    |       |
# +-------------+------------------+------+-----+---------+-------+
# CREATE TABLE post (
#     post_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     post TEXT NOT NULL,
#     photos TEXT,
#     post_time DATETIME NOT NULL,
#     modify_time DATETIME,
#     delete_time DATETIME,
#     heart INT UNSIGNED,
#     share INT UNSIGNED,
#     script INT UNSIGNED,
#     comment INT UNSIGNED,
#     hash VARCHAR(100)
# );


# pheart ( 게시물 하트 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | pheart_id | int(11)      | NO   | PRI | NULL    |       |
# | post_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE pheart (
#     pheart_id INT PRIMARY KEY NOT NULL,
#     post_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# share ( 게시물 공유 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | share_id  | int(11)      | NO   | PRI | NULL    |       |
# | post_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE share (
#     share_id INT PRIMARY KEY NOT NULL,
#     post_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# script ( 게시물 스크립트 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | script_id | int(11)      | NO   | PRI | NULL    |       |
# | post_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE script (
#     script_id INT PRIMARY KEY NOT NULL,
#     post_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# comment ( 게시물 댓글 )
# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | comment_id | int(11)      | NO   | PRI | NULL    |       |
# | post_id    | int(11)      | NO   | MUL | NULL    |       |
# | type       | tinyint(1)   | NO   |     | NULL    |       |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |       |
# | comment    | text         | NO   |     | NULL    |       |
# | cphoto     | longblob     | YES  |     | NULL    |       |
# | time       | datetime     | NO   |     | NULL    |       |
# | cheart     | int(11)      | YES  |     | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# CREATE TABLE comment (
#     comment_id INT PRIMARY KEY NOT NULL,
#     post_id INT NOT NULL,
#     type BOOL NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     comment TEXT NOT NULL,
#     cphoto LONGBLOB,
#     time DATETIME NOT NULL,
#     cheart INT,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# cheart ( 댓글 하트 )
# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | cheart_id  | int(11)      | NO   | PRI | NULL    |       |
# | comment_id | int(11)      | NO   | MUL | NULL    |       |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# CREATE TABLE cheart (
#     cheart_id INT PRIMARY KEY NOT NULL,
#     comment_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (comment_id) REFERENCES comment(comment_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# pregnancy ( 산모수첩 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | pregn_id  | int(11)      | NO   | PRI | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |       |
# | dname     | varchar(50)  | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE pregnancy (
#     pregn_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     dname VARCHAR(50),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );


# pregndaily ( 산모수첩 : 일기 )
# +----------+--------------+------+-----+---------+-------+
# | Field    | Type         | Null | Key | Default | Extra |
# +----------+--------------+------+-----+---------+-------+
# | daily_id | int(11)      | NO   | PRI | NULL    |       |
# | pregn_id | int(11)      | NO   | MUL | NULL    |       |
# | daily    | datetime     | NO   |     | NULL    |       |
# | title    | varchar(50)  | YES  |     | NULL    |       |
# | picture  | varchar(255) | YES  |     | NULL    |       |
# | post     | text         | YES  |     | NULL    |       |
# +----------+--------------+------+-----+---------+-------+
# CREATE TABLE pregndaily (
#     daily_id INT PRIMARY KEY NOT NULL,
#     pregn_id INT NOT NULL,
#     daily DATETIME NOT NULL,
#     title VARCHAR(50),
#     picture VARCHAR(255),
#     post TEXT,
#     FOREIGN KEY (pregn_id) REFERENCES pregnancy(pregn_id)
# );


# phospital ( 산모수첩 : 병원 )
# +-------------+--------------+------+-----+---------+-------+
# | Field       | Type         | Null | Key | Default | Extra |
# +-------------+--------------+------+-----+---------+-------+
# | hospital_id | int(11)      | NO   | PRI | NULL    |       |
# | pregn_id    | int(11)      | NO   | MUL | NULL    |       |
# | hday        | datetime     | NO   |     | NULL    |       |
# | parent_kg   | float        | NO   |     | NULL    |       |
# | bpressure   | float        | NO   |     | NULL    |       |
# | special     | varchar(50)  | YES  |     | NULL    |       |
# | baby_kg     | float        | YES  |     | NULL    |       |
# | baby_heart  | int(11)      | YES  |     | NULL    |       |
# | ultrasound  | varchar(255) | YES  |     | NULL    |       |
# | uvideo      | varchar(255) | YES  |     | NULL    |       |
# +-------------+--------------+------+-----+---------+-------+
# CREATE TABLE phospital (
#     hospital_id INT PRIMARY KEY NOT NULL,
#     pregn_id INT NOT NULL,
#     hday DATETIME NOT NULL,
#     parent_kg FLOAT NOT NULL,
#     bpressure FLOAT NOT NULL,
#     special VARCHAR(50),
#     baby_kg FLOAT,
#     baby_heart INT,
#     ultrasound VARCHAR(255),
#     uvideo VARCHAR(255),
#     FOREIGN KEY (pregn_id) REFERENCES pregnancy(pregn_id)
# );


# parenting ( 육아수첩 )
# +--------------+--------------+------+-----+---------+-------+
# | Field        | Type         | Null | Key | Default | Extra |
# +--------------+--------------+------+-----+---------+-------+
# | parenting_id | int(11)      | NO   | PRI | NULL    |       |
# | parent_id    | varchar(255) | NO   | MUL | NULL    |       |
# | baby_id      | varchar(255) | NO   | MUL | NULL    |       |
# | ptitle       | varchar(50)  | YES  |     | NULL    |       |
# +--------------+--------------+------+-----+---------+-------+
# CREATE TABLE parenting (
#     parenting_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     ptitle VARCHAR(50),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );


# pdaily ( 육아수첩 : 일기 )
# +--------------+--------------+------+-----+---------+-------+
# | Field        | Type         | Null | Key | Default | Extra |
# +--------------+--------------+------+-----+---------+-------+
# | daily_id     | int(11)      | NO   | PRI | NULL    |       |
# | parenting_id | int(11)      | NO   | MUL | NULL    |       |
# | daily        | datetime     | NO   |     | NULL    |       |
# | title        | varchar(50)  | YES  |     | NULL    |       |
# | picture      | varchar(255) | YES  |     | NULL    |       |
# | post         | text         | YES  |     | NULL    |       |
# +--------------+--------------+------+-----+---------+-------+
# CREATE TABLE pdaily (
#     daily_id INT PRIMARY KEY NOT NULL,
#     parenting_id INT NOT NULL,
#     daily DATETIME NOT NULL,
#     title VARCHAR(50),
#     picture VARCHAR(255),
#     post TEXT,
#     FOREIGN KEY (parenting_id) REFERENCES parenting(parenting_id)
# );


# deal ( 아기용품 중고거래 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | deal_id   | int(11)      | NO   | PRI | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | title     | int(11)      | NO   |     | NULL    |       |
# | post      | text         | YES  |     | NULL    |       |
# | img       | varchar(255) | NO   |     | NULL    |       |
# | time      | datetime     | NO   |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE deal (
#     deal_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     title INT NOT NULL,
#     post TEXT,
#     img VARCHAR(255) NOT NULL,
#     time DATETIME NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# dheart ( 중고거래 위시리스트 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | dheart_id | int(11)      | NO   | PRI | NULL    |       |
# | deal_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE dheart (
#     dheart_id INT PRIMARY KEY NOT NULL,
#     deal_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (deal_id) REFERENCES deal(deal_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# purchase ( 공동구매 게시글 )
# +-------------+--------------+------+-----+---------+-------+
# | Field       | Type         | Null | Key | Default | Extra |
# +-------------+--------------+------+-----+---------+-------+
# | purchase_id | int(11)      | NO   | PRI | NULL    |       |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |       |
# | title       | int(11)      | NO   |     | NULL    |       |
# | post        | text         | YES  |     | NULL    |       |
# | img         | varchar(255) | NO   |     | NULL    |       |
# | time        | datetime     | NO   |     | NULL    |       |
# | link        | varchar(255) | NO   |     | NULL    |       |
# +-------------+--------------+------+-----+---------+-------+
# CREATE TABLE purchase (
#     purchase_id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     title INT NOT NULL,
#     post TEXT,
#     img VARCHAR(255) NOT NULL,
#     time DATETIME NOT NULL,
#     link VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# joint ( 공동구매 )
# +-------------+--------------+------+-----+---------+-------+
# | Field       | Type         | Null | Key | Default | Extra |
# +-------------+--------------+------+-----+---------+-------+
# | joint_id    | int(11)      | NO   | PRI | NULL    |       |
# | purchase_id | int(11)      | NO   | MUL | NULL    |       |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |       |
# +-------------+--------------+------+-----+---------+-------+
# CREATE TABLE joint (
#     joint_id INT PRIMARY KEY NOT NULL,
#     purchase_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (purchase_id) REFERENCES purchase(purchase_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


# babycry ( 울음 기록 )
# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | id         | int(11)      | NO   | PRI | NULL    |       |
# | baby_id    | varchar(255) | NO   |     | NULL    |       |
# | time       | datetime     | YES  |     | NULL    |       |
# | type       | varchar(50)  | YES  |     | NULL    |       |
# | audioid    | char(1)      | YES  |     | NULL    |       |
# | predictMap | json         | YES  |     | NULL    |       |
# | intensity  | varchar(50)  | YES  |     | NULL    |       |
# | duration   | float        | YES  |     | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# CREATE TABLE babycry (
#     id INT PRIMARY KEY NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     time DATETIME,
#     type VARCHAR(50),
#     audioid CHAR,
#     predictMap JSON,
#     intensity VARCHAR(50),
#     duration FLOAT
# );


# aidoctor ( ai 의사 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | id        | int(11)      | NO   | PRI | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | ask_id    | varchar(100) | YES  |     | NULL    |       |
# | res_id    | varchar(100) | YES  |     | NULL    |       |
# | haddr     | varchar(255) | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE aidoctor (
#     id INT PRIMARY KEY NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     ask_id VARCHAR(100),
#     res_id VARCHAR(100),
#     haddr VARCHAR(255)
# );
# ALTER TABLE aidoctor
#     ADD CONSTRAINT fk_parent_id FOREIGN KEY (parent_id) REFERENCES parent(parent_id);


# chat ( 채팅 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | room_id   | int(11)      | NO   | PRI | NULL    |       |
# | name      | varchar(100) | YES  |     | NULL    |       |
# | pid       | varchar(255) | YES  |     | NULL    |       |
# | parent_id | varchar(255) | NO   |     | NULL    |       |
# | end_chat  | varchar(255) | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE chat (
#     room_id INT PRIMARY KEY NOT NULL,
#     name VARCHAR(100),
#     pid VARCHAR(255),
#     parent_id VARCHAR(255) NOT NULL,
#     end_chat VARCHAR(255)
# );


# chatbubble ( 실시간 채팅 말풍선 )
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | chat_id   | int(11)      | NO   | PRI | NULL    |       |
# | room_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | time      | datetime     | YES  |     | NULL    |       |
# | chat_type | varchar(255) | YES  |     | NULL    |       |
# | content   | text         | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE chatbubble (
#     chat_id INT PRIMARY KEY NOT NULL,
#     room_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     time DATETIME,
#     chat_type VARCHAR(255),
#     content TEXT,
#     FOREIGN KEY (room_id) REFERENCES chat(room_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );
