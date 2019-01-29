CREATE TABLE `urls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_url` text NOT NULL,
  `short_url` varchar(1000) NOT NULL,
  `domain` varchar(1000) DEFAULT NULL,
  `added_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `hash_long_url` varchar(64) NOT NULL,
  `click_count` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  FULLTEXT KEY `FTIX_longUrl` (`long_url`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `url_pool` (
  `short_url` varchar(10) NOT NULL,
  PRIMARY KEY (`short_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `running_id` (
  `current_id` int(11) NOT NULL,
  PRIMARY KEY (`current_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
