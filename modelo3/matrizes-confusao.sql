-- Matrizes de confusão

SET @classificador = 'negativo', @jurado = 'negativo';
SET @classificador = 'neutro', @jurado = 'negativo';
SET @classificador = 'positivo', @jurado = 'negativo';
--
SET @classificador = 'negativo', @jurado = 'neutro';
SET @classificador = 'neutro', @jurado = 'neutro';
SET @classificador = 'positivo', @jurado = 'neutro';
--
SET @classificador = 'negativo', @jurado = 'positivo';
SET @classificador = 'neutro', @jurado = 'positivo';
SET @classificador = 'positivo', @jurado = 'positivo';


-- select r.id_comentario, r.classe as classificador, j.classe as jurado
SELECT count(1)
from resultado_classificacao r 
JOIN corpus_marcado5 j ON r.id_comentario = j.id_comentario
WHERE
	r.classe = @classificador
	AND j.classe = @jurado;