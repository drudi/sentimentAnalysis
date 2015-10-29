-- Busca a interseccao dos casos em que há discordancia entre o classificador e os jurados
SET @classificador = 'neutro';
SET @jurados = 'positivo';

SELECT @jurados;

SELECT 
j1.id_comentario, 
c.comentario_usuario,
cl.classe as classificador,
j1.classe as jurado1,
j2.classe as jurado2,
j3.classe as jurado3,
j4.classe as jurado4,
j5.classe as jurado5
from modelo3.resultado_classificacao cl
JOIN modelo2.classificacao_manual j1 ON (cl.id_comentario = j1.id_comentario AND j1.jurado_id = 1)
JOIN modelo2.classificacao_manual j2 ON (cl.id_comentario = j2.id_comentario AND j2.jurado_id = 2)
JOIN modelo2.classificacao_manual j3 ON (cl.id_comentario = j3.id_comentario AND j3.jurado_id = 3)
JOIN modelo2.classificacao_manual j4 ON (cl.id_comentario = j4.id_comentario AND j4.jurado_id = 4)
JOIN modelo2.classificacao_manual j5 ON (cl.id_comentario = j5.id_comentario AND j5.jurado_id = 5)
JOIN modelo2.comentarios c ON j1.id_comentario = c.id_comentario
WHERE
cl.classe = @classificador AND
j1.classe = @jurados AND 
j2.classe = @jurados AND
j3.classe = @jurados AND
j4.classe = @jurados AND
j5.classe = @jurados;
