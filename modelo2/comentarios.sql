-- Cria a tabela
CREATE TABLE modelo2.comentarios (
  `id_comentario` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `data_comentario` date DEFAULT NULL,
  `motivo_cancelamento` varchar(255) DEFAULT NULL,
  `nota_atribuida` int(11) DEFAULT NULL,
  `comentario_usuario` text,
  KEY `id_comentario_idx` (`id_comentario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

-- Popula a tabela com comentarios aleatorios
insert into modelo2.comentarios (select c.cancellation_id as id_comentario, 
       c.usr_id as id_usuarios,
       c.date_exclusion as data_comentario,
       c.reason_code as motivo_cancelamento,
       c.satisfaction_degree as nota_atribuida,
       cc.usr_comment as comentario_usuario
from
       cancellation.cancellation c join
       cancellation.cancellation_comment cc on c.cancellation_id = cc.cancellation_id
where 
    c.date_exclusion > '2013-01-01'
    and c.date_exclusion < '2013-07-01'
    and (length(cc.usr_comment) >= 50 OR lower(cc.usr_comment) IN ('bom', 'muito bom', 'ruim', 'muito ruim', 'ótimo', 'excelente', 'péssimo') )
order by rand()
limit 2500)

-- Criacao do grupo de controle, para anotação manual
CREATE TABLE modelo2.comentarios_controle (
  `id_comentario` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `data_comentario` date DEFAULT NULL,
  `motivo_cancelamento` varchar(255) DEFAULT NULL,
  `nota_atribuida` int(11) DEFAULT NULL,
  `comentario_usuario` text,
  `anotacao_manual` enum('negativo', 'positivo', 'neutro') DEFAULT NULL,
  `score_calculado` int(11) DEFAULT NULL,
  KEY `id_comentario_idx` (`id_comentario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

-- Populacao inicial da comentarios_controle
insert into modelo2.comentarios_controle (
    select id_comentario, 
       id_usuario,
       data_comentario,
       motivo_cancelamento,
       nota_atribuida,
       comentario_usuario,
       NULL,
       NULL
    from
       modelo2.comentarios
    order by rand()
    limit 150
    )

-- Tabelas para comentarios classificados:

CREATE TABLE `classificacao` (
  `id_classificacao` int(11) NOT NULL AUTO_INCREMENT,
  `id_comentario` int(11) NOT NULL,
  `classe` enum('negativo', 'neutro', 'positivo') NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`id_classificacao`),
  KEY `id_comentario_idx` (`id_comentario`),
  KEY `classe_idx` (`classe`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1

CREATE TABLE `classificacao_controle` (
  `id_classificacao` int(11) NOT NULL AUTO_INCREMENT,
  `id_comentario` int(11) NOT NULL,
  `classe` enum('negativo', 'neutro', 'positivo') NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`id_classificacao`),
  KEY `id_comentario_idx` (`id_comentario`),
  KEY `classe_idx` (`classe`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1

-- Queries para montar as matrizes de confusão (exemplos)

-- Jurado com jurado
SELECT  count(1) FROM modelo2.classificacao_manual t1 join modelo2.classificacao_manual t2 
ON t1.id_comentario = t2.id_comentario
where
t1.jurado_id = 4 AND
t2.jurado_id = 5 AND
t1.classe = 'positivo' AND
t2.classe = 'positivo'

-- Com o classificador
SELECT count(cc.id_comentario) from classificacao_controle cc 
JOIN classificacao_manual cm 
ON cc.id_comentario = cm.id_comentario
where
cm.jurado_id = 1 AND
cm.classe = 'positivo' AND
cc.classe = 'positivo'

-- -----------------------------------------------------------------

CREATE TABLE `corpus_treinamento` (
  `id_comentario` int(11) NOT NULL,
  `comentario_usuario` text,
  `classe` enum('negativo','neutro','positivo') DEFAULT NULL,
  KEY `id_comentario_idx` (`id_comentario`),
  KEY `classe_idx` (`classe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into corpus_treinamento 
  select id_comentario, comentario_usuario, null 
  from modelo2.comentarios 
  where id_comentario not in (select id_comentario from modelo3.corpus_marcado) 
  order by rand() 
  limit 600;

-- ------------------------------------------------------------------

CREATE TABLE `corpus_marcado` (
  `id_comentario` int(11) NOT NULL,
  `comentario_usuario` text,
  `classe` enum('negativo','neutro','positivo') NOT NULL,
  KEY `id_comentario_idx` (`id_comentario`),
  KEY `classe_idx` (`classe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into corpus_marcado 
  select cm.id_comentario, c.comentario_usuario, cm.classe 
  from modelo2.classificacao_manual cm
  JOIN modelo2.comentarios c ON cm.id_comentario = c.id_comentario 
  where cm.jurado_id = 1;

------

CREATE TABLE `corpus_marcado2` (
  `id_comentario` int(11) NOT NULL,
  `comentario_usuario` text,
  `classe` enum('negativo','neutro','positivo') NOT NULL,
  KEY `id_comentario_idx` (`id_comentario`),
  KEY `classe_idx` (`classe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into corpus_marcado2 
  select cm.id_comentario, c.comentario_usuario, cm.classe 
  from modelo2.classificacao_manual cm
  JOIN modelo2.comentarios c ON cm.id_comentario = c.id_comentario 
  where cm.jurado_id = 2;
