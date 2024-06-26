INSERT INTO classifiers_identifier_type (id, type_name) VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'ISIN'),
(6, 'BBG Ticker'),
(7, 'Sedol'),
(8, 'RIC'),
(9, 'Internal Ticker'),
(10, 'BBG Exchange Code'),
(11, 'CIK'),
(12, 'FIGI');

INSERT INTO classifiers_instrument_class (id, instrument_type, instrument_class) VALUES
(1, 'Unknown','Unknown'),
(2, 'Unspecified','Unspecified'),
(3, 'None','None'),
(4, 'Other','Other'),
(5, 'Equity', 'Common Stock');

INSERT INTO classifiers_currency (id, major_unit, minor_unit, major_to_minor, ISO) VALUES
(1, 'Unknown','Unknown',0,'XYZ'),
(2, 'Unspecified','Unspecified',0,'XZY'),
(3, 'None','None',0,'YXZ'),
(4, 'Other','Other',0,'YZX'),
(5, 'United States Dollar', 'Cent', 100, 'USD'),
(6, 'Euro', 'Cent', 100, 'EUR'),
(7, 'Pound sterling', 'Pence', 100, 'GBP'),
(8, 'Swiss frank', 'Rappen/Centime', 1000, 'CHF'),
(9, 'Japanese yen', 'Sen', 100, 'JPY'),
(10,'Afghan afghani','Pul',100,'AFN'),
(11,'Albanian lek','Qintar',100,'ALL'),
(12,'Algerian dinar','Centime',100,'DZD'),
(13,'Angolan kwanza','Centimo',100,'AOA'),
(14,'Argentine peso','Centavo',100,'ARS'),
(15,'Armenian dram','Luma',100,'AMD'),
(16,'Aruban florin','Cent',100,'AWG'),
(17,'Australian dollar','Cent',100,'AUD'),
(18,'Azerbaijani manat','Qepik',100,'AZN'),
(19,'Bahamian dollar','Cent',100,'BSD'),
(20,'Bahraini dinar','Fils',1000,'BHD'),
(21,'Bangladeshi taka','Poisha',100,'BDT'),
(22,'Barbadian dollar','Cent',100,'BBD'),
(23,'Belarusian ruble','Kopeck',100,'BYN'),
(24,'Belize dollar','Cent',100,'BZD'),
(25,'Bermudian dollar','Cent',100,'BMD'),
(26,'Bhutanese ngultrum','Chetrum',100,'BTN'),
(27,'Bolivian boliviano','Centavo',100,'BOB'),
(28,'Bosnia and Herzegovina convertible mark','Fening',100,'BAM'),
(29,'Botswana pula','Thebe',100,'BWP'),
(30,'Brazilian real','Centavo',100,'BRL'),
(31,'Brunei dollar','Sen',100,'BND'),
(32,'Bulgarian lev','Stotinka',100,'BGN'),
(33,'Burmese kyat','Pya',100,'MMK'),
(34,'Burundian franc','Centime',100,'BIF'),
(35,'Cambodian riel','Sen',100,'KHR'),
(36,'Canadian dollar','Cent',100,'CAD'),
(37,'Cape Verdean escudo','Centavo',100,'CVE'),
(38,'Cayman Islands dollar','Cent',100,'KYD'),
(39,'Central African CFA franc','Centime',100,'XAF'),
(40,'CFP franc','Centime',100,'XPF'),
(41,'Chilean peso','Centavo',100,'CLP'),
(42,'Colombian peso','Centavo',100,'COP'),
(43,'Comorian franc','Centime',100,'KMF'),
(44,'Congolese franc','Centime',100,'CDF'),
(45,'Costa Rican colon','Centimo',100,'CRC'),
(46,'Cuban peso','Centavo',100,'CUP'),
(47,'Czech koruna','Heller',100,'CZK'),
(48,'Danish krone','Ore',100,'DKK'),
(49,'Djiboutian franc','Centime',100,'DJF'),
(50,'Dominican peso','Centavo',100,'DOP'),
(51,'Eastern Caribbean dollar','Cent',100,'XCD'),
(52,'Egyptian pound','Piastre',100,'EGP'),
(53,'Eritrean nakfa','Cent',100,'ERN'),
(54,'Ethiopian birr','Santim',100,'ETB'),
(55,'Falkland Islands pound','Penny',100,'FKP'),
(56,'Fijian dollar','Cent',100,'FJD'),
(57,'Gambian dalasi','Butut',100,'GMD'),
(58,'Georgian lari','Tetri',100,'GEL'),
(59,'Ghanaian cedi','Pesewa',100,'GHS'),
(60,'Gibraltar pound','Penny',100,'GIP'),
(61,'Guatemalan quetzal','Centavo',100,'GTQ'),
(62,'Guinean franc','Centime',100,'GNF'),
(63,'Guyanese dollar','Cent',100,'GYD'),
(64,'Haitian gourde','Centime',100,'HTG'),
(65,'Honduran lempira','Centavo',100,'HNL'),
(66,'Hong Kong dollar','Cent',100,'HKD'),
(67,'Hungarian forint','Filler',100,'HUF'),
(68,'Icelandic krona','Eyrir',100,'ISK'),
(69,'Indian rupee','Paisa',100,'INR'),
(70,'Indonesian rupiah','Sen',100,'IDR'),
(71,'Iranian rial','Rial',1,'IRR'),
(72,'Iraqi dinar','Fils',1000,'IQD'),
(73,'Israeli new shekel','Agora',100,'ILS'),
(74,'Jamaican dollar','Cent',100,'JMD'),
(75,'Jordanian dinar','Piastre',100,'JOD'),
(76,'Kazakhstani tenge','Tıyn',100,'KZT'),
(77,'Kenyan shilling','Cent',100,'KES'),
(78,'Kuwaiti dinar','Fils',1000,'KWD'),
(79,'Kyrgyz som','Tyiyn',100,'KGS'),
(80,'Lao kip','Att',100,'LAK'),
(81,'Lebanese pound','Piastre',100,'LBP'),
(82,'Lesotho loti','Sente',100,'LSL'),
(83,'Liberian dollar','Cent',100,'LRD'),
(84,'Libyan dinar','Dirham',1000,'LYD'),
(85,'Macanese pataca','Avo',100,'MOP'),
(86,'Macedonian denar','Deni',100,'MKD'),
(87,'Malagasy ariary','Iraimbilanja',5,'MGA'),
(88,'Malawian kwacha','Tambala',100,'MWK'),
(89,'Malaysian ringgit','Sen',100,'MYR'),
(90,'Maldivian rufiyaa','Laari',100,'MVR'),
(91,'Mauritanian ouguiya','Khoums',5,'MRU'),
(92,'Mauritian rupee','Cent',100,'MUR'),
(93,'Mexican peso','Centavo',100,'MXN'),
(94,'Moldovan leu','Ban',100,'MDL'),
(95,'Mongolian togrog','Mongo',100,'MNT'),
(96,'Moroccan dirham','Centime',100,'MAD'),
(97,'Mozambican metical','Centavo',100,'MZN'),
(98,'Namibian dollar','Cent',100,'NAD'),
(99,'Nepalese rupee','Paisa',100,'NPR'),
(100,'Netherlands Antillean guilder','Cent',100,'ANG'),
(101,'New Taiwan dollar','Cent',100,'TWD'),
(102,'New Zealand dollar','Cent',100,'NZD'),
(103,'Nicaraguan cordoba','Centavo',100,'NIO'),
(104,'Nigerian naira','Kobo',100,'NGN'),
(105,'North Korean won','Chon',100,'KPW'),
(106,'Norwegian krone','Ore',100,'NOK'),
(107,'Omani rial','Baisa',1000,'OMR'),
(108,'Pakistani rupee','Paisa',100,'PKR'),
(109,'Panamanian balboa','Centesimo',100,'PAB'),
(110,'Papua New Guinean kina','Toea',100,'PGK'),
(111,'Paraguayan guarani','Centimo',100,'PYG'),
(112,'Peruvian sol','Centimo',100,'PEN'),
(113,'Philippine peso','Sentimo',100,'PHP'),
(114,'Polish zloty','Grosz',100,'PLN'),
(115,'Qatari riyal','Dirham',100,'QAR'),
(116,'Renminbi','Jiao',10,'CNY'),
(117,'Romanian leu','Ban',100,'RON'),
(118,'Russian ruble','Kopeck',100,'RUB'),
(119,'Rwandan franc','Centime',100,'RWF'),
(120,'Saint Helena pound','Penny',100,'SHP'),
(121,'Samoan tala','Sene',100,'WST'),
(122,'Sao Tomeand Principe dobra','Centimo',100,'STN'),
(123,'Saudi riyal','Halala',100,'SAR'),
(124,'Serbian dinar','Para',100,'RSD'),
(125,'Seychellois rupee','Cent',100,'SCR'),
(126,'Sierra Leonean leone','Cent',100,'SLE'),
(127,'Singapore dollar','Cent',100,'SGD'),
(128,'Solomon Islands dollar','Cent',100,'SBD'),
(129,'Somali shilling','Cent',100,'SOS'),
(130,'South African rand','Cent',100,'ZAR'),
(131,'South Korean won','Jeon',100,'KRW'),
(132,'South Sudanese pound','Piaster',100,'SSP'),
(133,'Sri Lankan rupee','Cent',100,'LKR'),
(134,'Sudanese pound','Piastre',100,'SDG'),
(135,'Surinamese dollar','Cent',100,'SRD'),
(136,'Swazi lilangeni','Cent',100,'SZL'),
(137,'Swedish krona','Ore',100,'SEK'),
(138,'Syrian pound','Piastre',100,'SYP'),
(139,'Tajikistani somoni','Diram',100,'TJS'),
(140,'Tanzanian shilling','Cent',100,'TZS'),
(141,'Thai baht','Satang',100,'THB'),
(142,'Tongan paanga','Seniti',100,'TOP'),
(143,'Trinidad and Tobago dollar','Cent',100,'TTD'),
(144,'Tunisian dinar','Millime',1000,'TND'),
(145,'Turkish lira','Kurus',100,'TRY'),
(146,'Turkmenistani manat','Tenge',100,'TMT'),
(147,'Ukrainian hryvnia','Kopeck',100,'UAH'),
(148,'United Arab Emirates dirham','Fils',100,'AED'),
(149,'Uruguayan peso','Centesimo',100,'UYU'),
(150,'Uzbekistani sum','Tiyin',100,'UZS'),
(151,'Vanuatu vatu','Cent',100,'VUV'),
(152,'Venezuelan digital bolivar','Centimo',100,'VED'),
(153,'Venezuelan sovereign bolivar','Centimo',1,'VES'),
(154,'Vietnamese dong','Hao',10,'VND'),
(155,'West African CFA franc','Centime',100,'XOF'),
(156,'Yemeni rial','Fils',100,'YER'),
(157,'Zambian kwacha','Ngwee',100,'ZMW'),
(158,'Ugandan shilling','',0,'UGX');

update classifiers_currency
set active = 1
where id < 10 and id > 4;

INSERT INTO classifiers_country (id, name, short_name, ISO2, ISO3, ccy_id) VALUES
(1, 'Unknown','Unknown','XX','XYZ',1),
(2, 'Unspecified','Unspecified','YY','XZY',2),
(3, 'None','None','XY','YXZ',3),
(4, 'Other','Other','ZZ','YZX',4),
(5, 'The United States of America', 'USA', 'US', 'USA', 5),
(6, 'The Federal Republic of Germany', 'Germany', 'DE', 'DEU' , 6),
(7, 'The United Kingdom of Great Britain and Northern Ireland', 'UK', 'GB', 'GBR' , 7),
(8, 'The Swiss Confederation', 'Switzerland', 'CH', 'CHE' , 8),
(9, 'Japan', 'Japan', 'JP', 'JPN', 9),
(10,'The Islamic Republic of Afghanistan','Afghanistan','AF','AFG',10),
(11,'Aland','Aland Islands','AX','ALA',5),
(12,'The Republic of Albania','Albania','AL','ALB',11),
(13,'The Peoples Democratic Republic of Algeria','Algeria','DZ','DZA',12),
(14,'The Territory of American Samoa','American Samoa','AS','ASM',5),
(15,'The Principality of Andorra','Andorra','AD','AND',6),
(16,'The Republic of Angola','Angola','AO','AGO',13),
(17,'Anguilla','Anguilla','AI','AIA',51),
(18,'Antarctica (all land and ice shelves south of the60th parallel south)','Antarctica','AQ','ATA',3),
(19,'Antigua and Barbuda','Antigua and Barbuda','AG','ATG',51),
(20,'The Argentine Republic','Argentina','AR','ARG',14),
(21,'The Republic of Armenia','Armenia','AM','ARM',15),
(22,'Aruba','Aruba','AW','ABW',16),
(23,'The Commonwealth of Australia','Australia','AU','AUS',17),
(24,'The Republic of Austria','Austria','AT','AUT',6),
(25,'The Republic of Azerbaijan','Azerbaijan','AZ','AZE',18),
(26,'The Commonwealth of The Bahamas','Bahamas','BS','BHS',19),
(27,'The Kingdom of Bahrain','Bahrain','BH','BHR',20),
(28,'The Peopls Republic of Bangladesh','Bangladesh','BD','BGD',21),
(29,'Barbados','Barbados','BB','BRB',22),
(30,'The Republic of Belarus','Belarus','BY','BLR',23),
(31,'The Kingdom of Belgium','Belgium','BE','BEL',6),
(32,'Belize','Belize','BZ','BLZ',24),
(33,'The Republic of Benin','Benin','BJ','BEN',155),
(34,'Bermuda','Bermuda','BM','BMU',25),
(35,'The Kingdom of Bhutan','Bhutan','BT','BTN',26),
(36,'The Plurinational State of Bolivia','Bolivia','BO','BOL',27),
(37,'Bonaire, Sint Eustatius and Saba','Bonaire','BQ','BES',5),
(38,'Bosnia and Herzegovina','Bosnia and Herzegovina','BA','BIH',28),
(39,'The Republic of Botswana','Botswana','BW','BWA',29),
(40,'The Federative Republic of Brazil','Brazil','BR','BRA',30),
(41,'The British Indian Ocean Territory','British Indian Ocean Territory','IO','IOT',5),
(42,'The Nation of Brunei, the Abode of Peace','Brunei Darussalam','BN','BRN',31),
(43,'The Republic of Bulgaria','Bulgaria','BG','BGR',32),
(44,'Burkina Faso','Burkina Faso','BF','BFA',155),
(45,'The Republic of Burundi','Burundi','BI','BDI',34),
(46,'The Republic of Cabo Verde','Cape Verde','CV','CPV',37),
(47,'The Kingdom of Cambodia','Cambodia','KH','KHM',35),
(48,'The Republic of Cameroon','Cameroon','CM','CMR',39),
(49,'Canada','Canada','CA','CAN',36),
(50,'The Cayman Islands','Cayman Islanda','KY','CYM',38),
(51,'The Central African Republic','Central African Republic','CF','CAF',39),
(52,'The Republic of Chad','Chad','TD','TCD',39),
(53,'The Republic of Chile','Chile','CL','CHL',41),
(54,'The Peoples Republic of China','China','CN','CHN',116),
(55,'The Territory of Christmas Island','Christmas Island','CX','CXR',17),
(56,'The Territory of Cocos (Keeling) Islands','Cocos Islands','CC','CCK',17),
(57,'The Republic of Colombia','Colombia','CO','COL',42),
(58,'The Union of the Comoros','Comoros','KM','COM',43),
(59,'The Democratic Republic of the Congo','Congo Democratic Republic','CD','COD',44),
(60,'The Republic of the Congo','Congo','CG','COG',39),
(61,'The Cook Islands','Cook Islands','CK','COK',102),
(62,'The Republic of Costa Rica','Costa Rica','CR','CRI',45),
(63,'The Republic of Cote dIvoire','Cote dIvoire','CI','CIV',155),
(64,'The Republic of Croatia','Croatia','HR','HRV',6),
(65,'The Republic of Cuba','Cuba','CU','CUB',46),
(66,'The Country of Curacao','Curacao','CW','CUW',100),
(67,'The Republic of Cyprus','Cyprus','CY','CYP',6),
(68,'The Czech Republic','Czechia','CZ','CZE',47),
(69,'The Kingdom of Denmark','Denmark','DK','DNK',48),
(70,'The Republic of Djibouti','Djibouti','DJ','DJI',49),
(71,'The Commonwealth of Dominica','Dominica','DM','DMA',51),
(72,'The Dominican Republic','Dominican Republic','DO','DOM',50),
(73,'The Republic of Ecuador','Ecuador','EC','ECU',5),
(74,'The Arab Republic of Egypt','Egypt','EG','EGY',52),
(75,'The Republic of El Salvador','El Salvador','SV','SLV',5),
(76,'The Republic of Equatorial Guinea','Equatorial Guinea','GQ','GNQ',39),
(77,'The State of Eritrea','Eritrea','ER','ERI',53),
(78,'The Republic of Estonia','Estonia','EE','EST',6),
(79,'The Kingdom of Eswatini','Eswatini','SZ','SWZ',136),
(80,'The Federal Democratic Republic of Ethiopia','Ethiopia','ET','ETH',54),
(81,'The Falkland Islands','Falkland Islands','FK','FLK',7),
(82,'The Faroe Islands','Faroe Islands','FO','FRO',48),
(83,'The Republic of Fiji','Fiji','FJ','FJI',56),
(84,'The Republic of Finland','Finland','FI','FIN',6),
(85,'The French Republic','France','FR','FRA',6),
(86,'Guyane','French Guiana','GF','GUF',6),
(87,'French Polynesia','French Polynesia','PF','PYF',40),
(88,'The French Southern and Antarctic Lands','French Southern Territories','TF','ATF',6),
(89,'The Gabonese Republic','Gabon','GA','GAB',39),
(90,'The Republic of The Gambia','Gambia','GM','GMB',57),
(91,'Georgia','Georgia','GE','GEO',58),
(92,'The Republic of Ghana','Ghana','GH','GHA',59),
(93,'Gibraltar','Gibraltar','GI','GIB',7),
(94,'The Hellenic Republic','Greece','GR','GRC',6),
(95,'Kalaallit Nunaat','Greenland','GL','GRL',48),
(96,'Grenada','Grenada','GD','GRD',51),
(97,'Guadeloupe','Guadeloupe','GP','GLP',6),
(98,'The Territory of Guam','Guam','GU','GUM',5),
(99,'The Republic of Guatemala','Guatemala','GT','GTM',61),
(100,'The Bailiwick of Guernsey','Guernsey','GG','GGY',7),
(101,'The Republic of Guinea','Guinea','GN','GIN',62),
(102,'The Republic of Guinea-Bissau','Guinea-Bissau','GW','GNB',39),
(103,'The Co-operative Republic of Guyana','Guyana','GY','GUY',63),
(104,'The Republic of Haiti','Haiti','HT','HTI',64),
(105,'The Territory of Heard Island and McDonald Islands','Heard Island and McDonald Islands','HM','HMD',17),
(106,'The Holy See','Holy See','VA','VAT',6),
(107,'The Republic of Honduras','Honduras','HN','HND',65),
(108,'The Hong Kong Special Administrative Region of China','Hong Kong','HK','HKG',66),
(109,'Hungary','Hungary','HU','HUN',67),
(110,'Iceland','Iceland','IS','ISL',68),
(111,'The Republic of India','India','IN','IND',69),
(112,'The Republic of Indonesia','Indonesia','ID','IDN',70),
(113,'The Islamic Republic of Iran','Iran','IR','IRN',71),
(114,'The Republic of Iraq','Iraq','IQ','IRQ',72),
(115,'Ireland','Ireland','IE','IRL',6),
(116,'The Isle of Man','Isle of Man','IM','IMN',7),
(117,'The State of Israel','Israel','IL','ISR',73),
(118,'The Italian Republic','Italy','IT','ITA',6),
(119,'Jamaica','Jamaica','JM','JAM',74),
(120,'The Bailiwick of Jersey','Jersey','JE','JEY',7),
(121,'The Hashemite Kingdom of Jordan','Jordan','JO','JOR',75),
(122,'The Republic of Kazakhstan','Kazakhstan','KZ','KAZ',76),
(123,'The Republic of Kenya','Kenya','KE','KEN',77),
(124,'The Republic of Kiribati','Kiribati','KI','KIR',17),
(125,'The Democratic Peoples Republic of Korea','North Korea','KP','PRK',105),
(126,'The Republic of Korea','South Korea','KR','KOR',131),
(127,'The State of Kuwait','Kuwait','KW','KWT',78),
(128,'The Kyrgyz Republic','Kyrgyzstan','KG','KGZ',79),
(129,'The Lao Peoples Democratic Republic','Lao Peoples Democratic Republic','LA','LAO',80),
(130,'The Republic of Latvia','Latvia','LV','LVA',6),
(131,'The Lebanese Republic','Lebanon','LB','LBN',81),
(132,'The Kingdom of Lesotho','Lesotho','LS','LSO',82),
(133,'The Republic of Liberia','Liberia','LR','LBR',83),
(134,'The State of Libya','Libya','LY','LBY',84),
(135,'The Principality of Liechtenstein','Liechtenstein','LI','LIE',8),
(136,'The Republic of Lithuania','Lithuania','LT','LTU',6),
(137,'The Grand Duchy of Luxembourg','Luxembourg','LU','LUX',6),
(138,'The Macao Special Administrative Region of China','Macao','MO','MAC',66),
(139,'The Republic of Madagascar','Madagascar','MG','MDG',87),
(140,'The Republic of Malawi','Malawi','MW','MWI',88),
(141,'Malaysia','Malaysia','MY','MYS',89),
(142,'The Republic of Maldives','Maldives','MV','MDV',90),
(143,'The Republic of Mali','Mali','ML','MLI',155),
(144,'The Republic of Malta','Malta','MT','MLT',6),
(145,'The Republic of the Marshall Islands','Marshall Islands','MH','MHL',5),
(146,'Martinique','Martinique','MQ','MTQ',6),
(147,'The Islamic Republic of Mauritania','Mauritania','MR','MRT',91),
(148,'The Republic of Mauritius','Mauritius','MU','MUS',92),
(149,'The Department of Mayotte','Mayotte','YT','MYT',6),
(150,'The United Mexican States','Mexico','MX','MEX',93),
(151,'The Federated States of Micronesia','Micronesia','FM','FSM',5),
(152,'The Republic of Moldova','Moldova','MD','MDA',94),
(153,'The Principality of Monaco','Monaco','MC','MCO',6),
(154,'Mongolia','Mongolia','MN','MNG',95),
(155,'Montenegro','Montenegro','ME','MNE',6),
(156,'Montserrat','Montserrat','MS','MSR',51),
(157,'The Kingdom of Morocco','Morocco','MA','MAR',96),
(158,'The Republic of Mozambique','Mozambique','MZ','MOZ',97),
(159,'The Republic of the Union of Myanmar','Myanmar','MM','MMR',33),
(160,'The Republic of Namibia','Namibia','NA','NAM',98),
(161,'The Republic of Nauru','Nauru','NR','NRU',17),
(162,'The Federal Democratic Republic of Nepal','Nepal','NP','NPL',99),
(163,'The Kingdom of the Netherlands','Netherlands','NL','NLD',6),
(164,'New Caledonia','New Caledonia','NC','NCL',40),
(165,'New Zealand','New Zealand','NZ','NZL',102),
(166,'The Republic of Nicaragua','Nicaragua','NI','NIC',103),
(167,'The Republic of the Niger','Niger','NE','NER',155),
(168,'The Federal Republic of Nigeria','Nigeria','NG','NGA',103),
(169,'Niue','Niue','NU','NIU',102),
(170,'The Territory of Norfolk Island','Norfolk Island','NF','NFK',17),
(171,'The Republic of North Macedonia','North Macedonia','MK','MKD',86),
(172,'The Commonwealth of the Northern Mariana Islands','Northern Mariana Islands','MP','MNP',5),
(173,'The Kingdom of Norway','Norway','NO','NOR',106),
(174,'The Sultanate of Oman','Oman','OM','OMN',107),
(175,'The Islamic Republic of Pakistan','Pakistan','PK','PAK',108),
(176,'The Republic of Palau','Palau','PW','PLW',5),
(177,'The State of Palestine','Palestine','PS','PSE',75),
(178,'The Republic of Panama','Panama','PA','PAN',109),
(179,'The Independent State of Papua New Guinea','Papua New Guinea','PG','PNG',110),
(180,'The Republic of Paraguay','Paraguay','PY','PRY',111),
(181,'The Republic of Peru','Peru','PE','PER',112),
(182,'The Republic of the Philippines','Philippines','PH','PHL',113),
(183,'The Pitcairn, Henderson, Ducie and Oeno Islands','Pitcairn','PN','PCN',102),
(184,'The Republic of Poland','Poland','PL','POL',114),
(185,'The Portuguese Republic','Portugal','PT','PRT',6),
(186,'The Commonwealth of Puerto Rico','Puerto Rico','PR','PRI',5),
(187,'The State of Qatar','Qatar','QA','QAT',115),
(188,'Reunion','Reunion','RE','REU',5),
(189,'Romania','Romania','RO','ROU',117),
(190,'The Russian Federation','Russian Federation','RU','RUS',118),
(191,'The Republic of Rwanda','Rwanda','RW','RWA',119),
(192,'The Collectivity of Saint-Barthelemy','Saint Barthelemy','BL','BLM',6),
(193,'Saint Helena, Ascension and Tristan da Cunha','Saint Helena','SH','SHN',7),
(194,'Saint Kitts and Nevis','Saint Kitts and Nevis','KN','KNA',51),
(195,'Saint Lucia','Saint Lucia','LC','LCA',51),
(196,'The Collectivity of Saint-Martin','Saint Martin','MF','MAF',5),
(197,'The Overseas Collectivity of Saint-Pierre and Miquelon','Saint Pierre and Miquelon','PM','SPM',6),
(198,'Saint Vincent and the Grenadines','Saint Vincent and the Grenadines','VC','VCT',51),
(199,'The Independent State of Samoa','Samoa','WS','WSM',121),
(200,'The Republic of San Marino','San Marino','SM','SMR',6),
(201,'The Democratic Republic of Sao Tome and Principe','Sao Tome and Principe','ST','STP',122),
(202,'The Kingdom of Saudi Arabia','Saudi Arabia','SA','SAU',123),
(203,'The Republic of Senegal','Senegal','SN','SEN',155),
(204,'The Republic of Serbia','Serbia','RS','SRB',124),
(205,'The Republic of Seychelles','Seychelles','SC','SYC',125),
(206,'The Republic of Sierra Leone','Sierra Leone','SL','SLE',126),
(207,'The Republic of Singapore','Singapore','SG','SGP',127),
(208,'Sint Maarten','Sint Maarten','SX','SXM',100),
(209,'The Slovak Republic','Slovakia','SK','SVK',6),
(210,'The Republic of Slovenia','Slovenia','SI','SVN',6),
(211,'The Solomon Islands','Solomon Islands','SB','SLB',128),
(212,'The Federal Republic of Somalia','Somalia','SO','SOM',129),
(213,'The Republic of South Africa','South Africa','ZA','ZAF',130),
(214,'South Georgia and the South Sandwich Islands','South Georgia Sandwich Islands','GS','SGS',7),
(215,'The Republic of South Sudan','South Sudan','SS','SSD',132),
(216,'The Kingdom of Spain','Spain','ES','ESP',6),
(217,'The Democratic Socialist Republic of Sri Lanka','Sri Lanka','LK','LKA',133),
(218,'The Republic of the Sudan','Sudan','SD','SDN',134),
(219,'The Republic of Suriname','Suriname','SR','SUR',135),
(220,'Svalbard and Jan Mayen','Svalbard','SJ','SJM',106),
(221,'The Kingdom of Sweden','Sweden','SE','SWE',137),
(222,'The Syrian Arab Republic','Syrian Arab Republic','SY','SYR',138),
(223,'Taiwan','Taiwan','TW','TWN',101),
(224,'The Republic of Tajikistan','Tajikistan','TJ','TJK',139),
(225,'The United Republic of Tanzania','Tanzania','TZ','TZA',140),
(226,'The Kingdom of Thailand','Thailand','TH','THA',141),
(227,'The Democratic Republic of Timor-Leste','East Timor','TL','TLS',5),
(228,'The Togolese Republic','Togo','TG','TGO',155),
(229,'Tokelau','Tokelau','TK','TKL',102),
(230,'The Kingdom of Tonga','Tonga','TO','TON',142),
(231,'The Republic of Trinidad and Tobago','Trinidad and Tobago','TT','TTO',143),
(232,'The Republic of Tunisia','Tunisia','TN','TUN',144),
(233,'The Republic of Turkiye','Turkey','TR','TUR',145),
(234,'Turkmenistan','Turkmenistan','TM','TKM',146),
(235,'The Turks and Caicos Islands','Turks and Caicos Islands','TC','TCA',5),
(236,'Tuvalu','Tuvalu','TV','TUV',17),
(237,'The Republic of Uganda','Uganda','UG','UGA',158),
(238,'Ukraine','Ukraine','UA','UKR',147),
(239,'The United Arab Emirates','UAE','AE','ARE',148),
(240,'BakerIsland,HowlandIsland,JarvisIsland,JohnstonAtoll,KingmanReef,MidwayAtoll,NavassaIsland,PalmyraAtoll, andWakeIsland','United States Minor Outlying Islands','UM','UMI',5),
(241,'The Oriental Republic of Uruguay','Uruguay','UY','URY',149),
(242,'The Republic of Uzbekistan','Uzbekistan','UZ','UZB',150),
(243,'The Republic of Vanuatu','Vanuatu','VU','VUT',151),
(244,'The Bolivarian Republic of Venezuela','Venezuela','VE','VEN',153),
(245,'The Socialist Republic of Viet Nam','Viet Nam','VN','VNM',154),
(246,'The British Virgin Islands','British Virgin Islands','VG','VGB',5),
(247,'The Virgin Islands of the United States','Virgin Islands','VI','VIR',5),
(248,'The Territory of the Wallis and Futuna Islands','Wallis and Futuna','WF','WLF',40),
(249,'The Republic of Yemen','Yemen','YE','YEM',156),
(250,'The Republic of Zambia','Zambia','ZM','ZMB',157),
(251,'The Republic of Zimbabwe','Zimbabwe','ZW','ZWE',5);

update classifiers_country
set active = 1
where id < 10;

INSERT INTO classifiers_organization_type (id, type_name) VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'Public'),
(6, 'Headquarters'),
(7, 'Fund'),
(8, 'Issuer'),
(9, 'Prime Broker'),
(10, 'Counterparty');

INSERT INTO classifiers_industry_sector (id, sector_name) VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'Automotive'),
(6, 'Telecommunications');

INSERT INTO classifiers_industry_subsector (id, subsector_name, sector_id) VALUES
(1, 'Unknown',1),
(2, 'Unspecified',2),
(3, 'None',3),
(4, 'Other',4),
(5, 'Automotive', 5),
(6, 'Telecommunications', 6);

INSERT INTO classifiers_market_data_source (id, source_name, function_name) VALUES
(1, 'Unknown',''),
(2, 'Unspecified',''),
(3, 'None',''),
(4, 'Other',''),
(5, 'Yahoo Finance Prices','get_yf_price_data');

INSERT INTO classifiers_accounting_method (id, method_name, description) VALUES
(1, 'FIFO', 'First In, First Out'),
(2, 'Weighted Avg', 'Weighted Average Accounting');

INSERT INTO classifiers_trade_status (code, name, description) VALUES 
('N', 'New', 'New trade'),
('X', 'Cancelled', 'Cancelled trade'),
('R', 'Reversal', 'Reversal of a cancelled trade'),
('A', 'Amended', 'Amendment of another trade');