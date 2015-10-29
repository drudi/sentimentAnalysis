CREATE TABLE `comentarios_traduzidos` (
  `id_comentario` int(11) NOT NULL,
  `comentario_usuario` text,
  `comentario_traduzido` text,
  KEY `id_comentario_idx` (`id_comentario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 SELECT id_comentario, comentario_usuario FROM modelo2.comentarios;



