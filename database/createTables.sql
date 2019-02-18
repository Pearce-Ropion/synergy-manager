-- Stores information about individual users
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    userID VARCHAR(40) NOT NULL,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password BINARY(60) NOT NULL,
    family_size INT,
    PRIMARY KEY (id)
);

-- Stores channel usage data where each channel's usage is associated with its device's ID
CREATE TABLE usages (
	id INT NOT NULL AUTO_INCREMENT,
	deviceID VARCHAR(40) NOT NULL,
	time INT,
	ch1 DOUBLE(5,3),
	ch2 DOUBLE(5,3),
	ch3 DOUBLE(5,3),
	ch4 DOUBLE(5,3),
	ch5 DOUBLE(5,3),
	ch6 DOUBLE(5,3),
	ch7 DOUBLE(5,3),
	ch8 DOUBLE(5,3),
	ch9 DOUBLE(5,3),
	ch10 DOUBLE(5,3),
	ch11 DOUBLE(5,3),
	ch12 DOUBLE(5,3),
	PRIMARY KEY (id)
);

-- Stores device name and deviceID to channelID association
CREATE TABLE devices (
	id INT NOT NULL AUTO_INCREMENT,
	deviceID VARCHAR(40) NOT NULL,
	name VARCHAR(20),
	ch1 VARCHAR(40),
	ch2 VARCHAR(40),
	ch3 VARCHAR(40),
	ch4 VARCHAR(40),
	ch5 VARCHAR(40),
	ch6 VARCHAR(40),
	ch7 VARCHAR(40),
	ch8 VARCHAR(40),
	ch9 VARCHAR(40),
	ch10 VARCHAR(40),
	ch11 VARCHAR(40),
	ch12 VARCHAR(40),
	PRIMARY KEY (id)
);

-- Stores channelID to channel name association
CREATE TABLE channels (
	id INT NOT NULL AUTO_INCREMENT,
	deviceID VARCHAR(40) NOT NULL,
	channelID VARCHAR(40) NOT NULL,
	name VARCHAR(20),
	PRIMARY KEY (id)
);

-- Stores which UUIDs (could be deviceID, channelID or groupID) are associated with each group
CREATE TABLE groupings (
	id INT NOT NULL AUTO_INCREMENT,
	groupID VARCHAR(40) NOT NULL,
	uuid VARCHAR(40) NOT NULL,
	PRIMARY KEY (id)
);

-- Stores group IDs with their associated name
CREATE TABLE groups (
	id INT NOT NULL AUTO_INCREMENT,
	groupID VARCHAR(40) NOT NULL,
	name VARCHAR(20),
	PRIMARY KEY (id)
);