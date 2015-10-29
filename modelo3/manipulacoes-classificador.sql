SELECT * FROM modelo3.resultado_classificacao;

update resultado_classificacao set classe = null;

-- Calcula concordancia
select r.id_comentario, r.classe as classificador, j.classe as jurado
from resultado_classificacao r 
JOIN corpus_marcado4 j ON r.id_comentario = j.id_comentario
WHERE
	r.classe = j.classe;

-- Positivo positivo
select r.id_comentario, r.classe as classificador, j.classe as jurado
from resultado_classificacao r 
JOIN corpus_marcado4 j ON r.id_comentario = j.id_comentario
WHERE
	r.classe = 'neutro'
	-- AND j.classe = 'neutro';

