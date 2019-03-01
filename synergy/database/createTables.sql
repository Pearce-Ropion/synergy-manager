DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `usages`;
DROP TABLE IF EXISTS `devices`;
DROP TABLE IF EXISTS `channels`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `groupings`;

-- Stores information about individual users
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userID` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(40) NOT NULL,
  `password` binary(60) NOT NULL,
  `family_size` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `users` ADD UNIQUE (`userID`);

-- Stores channel usage data where each channel's usage is associated with its device's ID
CREATE TABLE `usages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceID` varchar(36) NOT NULL,
  `time` bigint(13) NOT NULL,
  `ch1` double(5,3) DEFAULT NULL,
  `ch2` double(5,3) DEFAULT NULL,
  `ch3` double(5,3) DEFAULT NULL,
  `ch4` double(5,3) DEFAULT NULL,
  `ch5` double(5,3) DEFAULT NULL,
  `ch6` double(5,3) DEFAULT NULL,
  `ch7` double(5,3) DEFAULT NULL,
  `ch8` double(5,3) DEFAULT NULL,
  `ch9` double(5,3) DEFAULT NULL,
  `ch10` double(5,3) DEFAULT NULL,
  `ch11` double(5,3) DEFAULT NULL,
  `ch12` double(5,3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `usages` ADD UNIQUE (`time`);

-- Stores device name and deviceID to channelID association
CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceID` varchar(36) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `ch1` varchar(36) NOT NULL,
  `ch2` varchar(36) DEFAULT NULL,
  `ch3` varchar(36) DEFAULT NULL,
  `ch4` varchar(36) DEFAULT NULL,
  `ch5` varchar(36) DEFAULT NULL,
  `ch6` varchar(36) DEFAULT NULL,
  `ch7` varchar(36) DEFAULT NULL,
  `ch8` varchar(36) DEFAULT NULL,
  `ch9` varchar(36) DEFAULT NULL,
  `ch10` varchar(36) DEFAULT NULL,
  `ch11` varchar(36) DEFAULT NULL,
  `ch12` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `devices` ADD UNIQUE (`deviceID`);

-- Stores channelID to channel name association
CREATE TABLE `channels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceID` varchar(36) NOT NULL,
  `channelID` varchar(36) NOT NULL,
  `position` int(2) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `channels` ADD UNIQUE (`channelID`);

-- Stores which UUIDs (could be deviceID, channelID or groupID) are associated with each group and its type
CREATE TABLE `groupings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` varchar(36) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `type` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Stores group IDs with their associated name
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` varchar(36) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `groups` ADD UNIQUE (`groupID`);

INSERT INTO `devices` (`deviceID`, `ch1`, `ch2`, `ch3`, `ch4`, `ch5`, `ch6`, `ch7`, `ch8`)
VALUES
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '909eec56-1423-4fd1-853c-0099c23e00d9', 'b3c66fad-7ed0-41b7-9a9b-338f4b96c988', '9afa3cfd-1d67-452f-bccf-0e3d5d3d39ed', '85a8c6cb-477b-4af9-9cd9-a3ea9258f1e4', 'd9f3efd6-592b-451b-99ec-dc81f3580268', '7afc770c-a064-491d-9188-1107e2ee0539', 'a96fa90d-274c-4cf3-92e8-b5efe582b441', '578567f6-b205-4168-929a-31c4518b6709'),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'e2daddbc-7f96-4fb9-bf89-3f850314fb69', '9f13059a-e849-44ac-b465-57ea0d0c24fd', 'ae81a9de-63dc-4494-8103-aca9c599e834', '1127b322-1a1d-4228-ba08-65e21a944273', '55e8e473-06ad-49da-ba70-d53a42a0e3f8', 'a7812f76-56e3-4b30-85e9-fa5d0c311272', '828ed4a6-1112-454f-a6c9-2b2819c7b409', 'cc6e4793-fd6b-45ff-9f6c-808a1ae436a5'),
	('510460ed-326e-401a-b123-0a34c20269ec', '1ea90df8-f3f5-4f08-b905-bb8daefe0643', '84dc9115-554d-4b72-b778-a1bd77ffc6cd', '4dda3fe5-d8fc-4f50-b100-f120e93d5091', '33021dfe-913c-4197-b3d9-3793b9f29cb9', '791d2dc2-26e9-49a9-829e-abb07b10b724', '747be907-ae3c-40bd-9ddc-9004f3e5ae24', '04a93fc2-2efc-459f-a481-914515d4c156', 'cbd86278-ece8-4b33-8ef5-c5062c85da43');

INSERT INTO `channels` (`deviceID`, `channelID`, `position`)
VALUES
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '909eec56-1423-4fd1-853c-0099c23e00d9', 1),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', 'b3c66fad-7ed0-41b7-9a9b-338f4b96c988', 2),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '9afa3cfd-1d67-452f-bccf-0e3d5d3d39ed', 3),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '85a8c6cb-477b-4af9-9cd9-a3ea9258f1e4', 4),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', 'd9f3efd6-592b-451b-99ec-dc81f3580268', 5),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '7afc770c-a064-491d-9188-1107e2ee0539', 6),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', 'a96fa90d-274c-4cf3-92e8-b5efe582b441', 7),
	('75479fe4-6c70-437a-bf10-731cbd58fbe9', '578567f6-b205-4168-929a-31c4518b6709', 8),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'e2daddbc-7f96-4fb9-bf89-3f850314fb69', 1),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', '9f13059a-e849-44ac-b465-57ea0d0c24fd', 2),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'ae81a9de-63dc-4494-8103-aca9c599e834', 3),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', '1127b322-1a1d-4228-ba08-65e21a944273', 4),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', '55e8e473-06ad-49da-ba70-d53a42a0e3f8', 5),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'a7812f76-56e3-4b30-85e9-fa5d0c311272', 6),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', '828ed4a6-1112-454f-a6c9-2b2819c7b409', 7),
	('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'cc6e4793-fd6b-45ff-9f6c-808a1ae436a5', 8),
	('510460ed-326e-401a-b123-0a34c20269ec', '1ea90df8-f3f5-4f08-b905-bb8daefe0643', 1),
	('510460ed-326e-401a-b123-0a34c20269ec', '84dc9115-554d-4b72-b778-a1bd77ffc6cd', 2),
	('510460ed-326e-401a-b123-0a34c20269ec', '4dda3fe5-d8fc-4f50-b100-f120e93d5091', 3),
	('510460ed-326e-401a-b123-0a34c20269ec', '33021dfe-913c-4197-b3d9-3793b9f29cb9', 4),
	('510460ed-326e-401a-b123-0a34c20269ec', '791d2dc2-26e9-49a9-829e-abb07b10b724', 5),
	('510460ed-326e-401a-b123-0a34c20269ec', '747be907-ae3c-40bd-9ddc-9004f3e5ae24', 6),
	('510460ed-326e-401a-b123-0a34c20269ec', '04a93fc2-2efc-459f-a481-914515d4c156', 7),
	('510460ed-326e-401a-b123-0a34c20269ec', 'cbd86278-ece8-4b33-8ef5-c5062c85da43', 8);

INSERT INTO `groups` (`groupID`, `name`)
VALUES
	('5c7bc693-509f-4904-af19-a35db2a2bdb4', 'GroupWithDevices'),
	('a75700a3-75b1-4e26-a4bf-392c9d6e0032', 'GroupWithGroups');

INSERT INTO `groupings` (`groupID`, `uuid`, `type`)
VALUES
	('5c7bc693-509f-4904-af19-a35db2a2bdb4', '85a8c6cb-477b-4af9-9cd9-a3ea9258f1e4', 'channel'),
	('5c7bc693-509f-4904-af19-a35db2a2bdb4', '67c3e144-d7c0-4f60-a8fe-04552d55e3b0', 'device'),
	('a75700a3-75b1-4e26-a4bf-392c9d6e0032', '5c7bc693-509f-4904-af19-a35db2a2bdb4', 'group'),
	('a75700a3-75b1-4e26-a4bf-392c9d6e0032', '4dda3fe5-d8fc-4f50-b100-f120e93d5091', 'channel');

INSERT INTO `users` (`userID`, `name`, `email`, `password`, `family_size`)
VALUES
	('f6ffcdaa-48fb-4782-9ed4-c5cec790123b', 'Synergy Admin', 'admin@synergy.com', '$2a$10$JD/SrONlfEdj/1WrQXIX1uQCRHvj.rJ9y3uas3TlrGrD2YRjRk052', 2);

INSERT INTO `usages` (`deviceID`, `time`, `ch1`, `ch2`, `ch3`, `ch4`, `ch5`, `ch6`, `ch7`, `ch8`)
VALUES
    ('75479fe4-6c70-437a-bf10-731cbd58fbe9', UNIX_TIMESTAMP(NOW(3))*1000, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1),
    ('67c3e144-d7c0-4f60-a8fe-04552d55e3b0', UNIX_TIMESTAMP(NOW(3))*1000 + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1),
    ('510460ed-326e-401a-b123-0a34c20269ec', UNIX_TIMESTAMP(NOW(3))*1000 + 2, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1, (RAND() * (16 - 1)) + 1);
