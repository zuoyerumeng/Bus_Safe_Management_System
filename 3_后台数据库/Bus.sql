-- 创建数据库
DROP DATABASE IF EXISTS bus; -- 若数据库已存在则删除
CREATE DATABASE bus;
USE bus;

-- 删除现有数据库
DROP TABLE IF EXISTS Route;
DROP TABLE IF EXISTS Driver;
DROP TABLE IF EXISTS Convoy;
DROP TABLE IF EXISTS Leader;
DROP TABLE IF EXISTS Bus;
DROP TABLE IF EXISTS Illegal;

-- 创建数据表（包括实体完整性、参照完整性、用户自定义完整性等完整性规则）
CREATE TABLE Leader -- 队长表
    (number_job INT PRIMARY KEY NOT NULL,
     name VARCHAR(30) NOT NULL,
     sex VARCHAR(2) NOT NULL CHECK (sex IN ('男','女')),
     age INT NOT NULL,
     phone_number BIGINT NOT NULL CHECK (phone_number BETWEEN 10000000000 AND 99999999999) UNIQUE,
     address VARCHAR(50) NOT NULL);

CREATE TABLE Convoy -- 车队表
    (number_convoy INT PRIMARY KEY NOT NULL, -- 车队编号
     number_job_leader INT NOT NULL,
     FOREIGN KEY (number_job_leader) REFERENCES Leader(number_job)); -- 队长工号

CREATE TABLE Route -- 线路表
    (number_route INT PRIMARY KEY NOT NULL, -- 线路编号
     number_job_routeleader INT NOT NULL); -- 路队长工号

CREATE TABLE Driver -- 司机表（包括路队长，但不包括队长）
    (number_job INT PRIMARY KEY NOT NULL, -- 工号
     number_route INT NOT NULL, -- 线路编号
     name VARCHAR(8) NOT NULL,
     sex VARCHAR(2) NOT NULL CHECK (sex IN ('男','女')),
     age INT NOT NULL CHECK (age BETWEEN 18 AND 60),
     phone_number BIGINT NOT NULL UNIQUE CHECK(phone_number BETWEEN 10000000000 AND 99999999999),
     address VARCHAR(50) NOT NULL,
     FOREIGN KEY (number_route) REFERENCES Route(number_route));

CREATE TABLE Bus -- 公交汽车表
    (number_bus VARCHAR(10) PRIMARY KEY NOT NULL, -- 车牌号
     number_convoy INT NOT NULL, -- 车队编号
     number_route INT NOT NULL, -- 线路编号
     size INT NOT NULL, -- 座数
     type VARCHAR(20) NOT NULL, -- 车型
     FOREIGN KEY (number_convoy) REFERENCES Convoy (number_convoy),
     FOREIGN KEY (number_route) REFERENCES Route (number_route));

CREATE TABLE Illegal -- 违章信息表
    (number_job INT NOT NULL, -- 工号
     name VARCHAR(30) NOT NULL, -- 姓名
     number_bus VARCHAR(10) NOT NULL, -- 车牌号
     number_convoy INT NOT NULL, -- 车队编号
     number_route INT NOT NULL, -- 线路编号
     site VARCHAR(20) NOT NULL, -- 站点
     time DATETIME NOT NULL, -- 时间
     illegal VARCHAR(20) NOT NULL, -- 违章信息
     FOREIGN KEY (number_job) REFERENCES Driver (number_job),
     FOREIGN KEY (number_bus) REFERENCES Bus (number_bus),
     FOREIGN KEY (number_convoy) REFERENCES Convoy (number_convoy),
     FOREIGN KEY (number_route) REFERENCES Route (number_route)); -- 违章表

-- 创建索引来加快查询的速度
CREATE INDEX index_convoy ON Convoy (number_convoy ASC) ;
CREATE INDEX index_route ON Route (number_route ASC);
CREATE INDEX index_leader ON Leader (number_job ASC);
CREATE INDEX index_bus ON Bus (number_bus ASC);
CREATE INDEX index_driver ON Driver (number_job ASC);

-- 创建视图来简化系统的设计
CREATE VIEW Route_leader
	AS
	SELECT * 
	FROM Driver
	WHERE number_job IN
	(SELECT number_job_routeleader FROM Route);

-- 录入信息
INSERT INTO Leader VALUES (1,'江昱峰','男',19,13914250795,'陕西省西安市西安电子科技大学南校区海棠十号楼二区302左室');
INSERT INTO Leader VALUES (2,'轻井泽','女',22,13921190025,'陕西省西安市西安电子科技大学南校区丁香十四号楼一区606右室');
INSERT INTO Convoy VALUES (1,1);
INSERT INTO Convoy VALUES (2,2);
INSERT INTO Route VALUES (1,3);
INSERT INTO Route VALUES (2,4);
INSERT INTO Bus VALUES ('陕A B107R',1,1,16,'新能源公交车');
INSERT INTO Bus VALUES ('陕A 12345',2,2,20,'混合动力公交车');
INSERT INTO Driver VALUES (3,1,'汪文轩','男',20,13914112452,'陕西省西安市西安电子科技大学南校区海棠十号楼二区302左室');
INSERT INTO Driver VALUES (4,2,'王俞钦','男',21,13914112453,'陕西省西安市西安电子科技大学南校区海棠十号楼二区304右室');
INSERT INTO Driver VALUES (5,1,'曾岩','男',21,13907951425,'陕西省西安市西安电子科技大学南校区海棠十号楼二区302左室');
INSERT INTO Driver VALUES (6,2,'张若石','男',20,13900252119,'陕西省西安市西安电子科技大学南校区海棠十号楼二区302左室');
INSERT INTO Illegal VALUES (3,'汪文轩','陕A B107R',1,1,'未来之瞳站','2023-12-13 15:31:30','闯红灯');
INSERT INTO Illegal VALUES (5,'曾岩','陕A 12345',1,1,'小寨站','2023-12-13 19:36:03','闯红灯');
