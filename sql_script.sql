CREATE TABLE `user` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(20) NOT NULL,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `userStatus` int NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `statusproduct` (
  `statusProduct` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`statusProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `statuscustom` (
  `statusCustom` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`statusCustom`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `production` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `number` int NOT NULL,
  `statusProductid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `statusProductid` (`statusProductid`),
  CONSTRAINT `production_ibfk_1` FOREIGN KEY (`statusProductid`) REFERENCES `statusproduct` (`statusProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `custom` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shipDate` datetime NOT NULL,
  `packed` tinyint(1) DEFAULT NULL,
  `statusCustomid` int DEFAULT NULL,
  `userid` int DEFAULT NULL,
  `productionid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `productionid` (`productionid`),
  KEY `statusCustomid` (`statusCustomid`),
  KEY `userid` (`userid`),
  CONSTRAINT `custom_ibfk_1` FOREIGN KEY (`productionid`) REFERENCES `production` (`id`),
  CONSTRAINT `custom_ibfk_2` FOREIGN KEY (`statusCustomid`) REFERENCES `statuscustom` (`statusCustom`),
  CONSTRAINT `custom_ibfk_3` FOREIGN KEY (`userid`) REFERENCES `user` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
SELECT * FROM inetshop.custom;