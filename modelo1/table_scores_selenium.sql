CREATE TABLE `scores_selenium` (
  `id_score` int(11) NOT NULL AUTO_INCREMENT,
  `id_comentario` int(11) NOT NULL,
  `comentario_traduzido` text,
  `score` decimal(7,5) default NULL,
  PRIMARY KEY (`id_score`),
  KEY `id_comentario_idx` (`id_comentario`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 SELECT 
 id_comentario, comentario_traduzido FROM analise.comentarios_traduzidos;

CREATE TABLE `comentarios_classificados` (
	`id_classificacao` int(11) NOT NULL AUTO_INCREMENT,
	`id_comentario` int(11) NOT NULL,
	`score` decimal(7,5) default NULL,
	`classe` enum('negativo','neutro','positivo') default NULL,
	PRIMARY KEY (`id_classificacao`),
	KEY `id_comentario_idx` (`id_comentario`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1
SELECT id_comentario, score FROM analise.scores_selenium;