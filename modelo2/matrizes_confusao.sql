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


SELECT  count(1)
FROM modelo2.classificacao_manual cm
JOIN modelo2.classificacao cc ON cm.id_comentario = cc.id_comentario
WHERE cm.jurado_id = 5
AND cm.classe = @jurado
AND cc.classe = @classificador;