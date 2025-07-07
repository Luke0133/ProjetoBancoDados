CREATE OR REPLACE VIEW tb_infoextensao AS
SELECT ext.codExt,tipoAcao,titulo,dep.sigla AS departamento,doc.nome AS Coordenador FROM tb_extensao ext
	JOIN tb_funcaodocente fdoc
	ON fdoc.codext = ext.codext
	JOIN tb_docente doc
	ON doc.matricula = fdoc.coddocente AND fdoc.funcao = 'Coordenador(a)'
	JOIN tb_departamento dep
	ON doc.CodDep = dep.CodDep;


CREATE OR REPLACE VIEW tb_feedback_detalhado AS
/* Tabela com todos os feedbacks de pessoas e informações relevantes da pessoa */
SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, p.Nome, fp.Funcao
FROM TB_Feedback f JOIN TB_FeedbackPessoa fpessoa 
  ON f.CodFeedback = fpessoa.CodFeedback
JOIN TB_Pessoa p 
  ON fpessoa.CodPessoa = p.CPF
LEFT JOIN TB_FuncaoPessoa fp 
  ON fp.CodPessoa = p.CPF AND fp.CodExt = f.CodExt

UNION ALL  /* União entre as tabelas (compatíveis pois nome e funcao são equivalentes em todas as tabelas) */

/* Tabela com todos os feedbacks de docentes e informações relevantes do docente */
SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, d.Nome, fd.Funcao
FROM TB_Feedback f JOIN TB_FeedbackDocente fdoc 
  ON f.CodFeedback = fdoc.CodFeedback
JOIN TB_Docente d 
  ON fdoc.CodDocente = d.Matricula
LEFT JOIN TB_FuncaoDocente fd 
  ON fd.CodDocente = d.Matricula AND fd.CodExt = f.CodExt

UNION ALL  /* União entre as tabelas (compatíveis pois nome e funcao são equivalentes em todas as tabelas) */

/* Tabela com todos os feedbacks de alunos e informações relevantes do aluno */
SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, a.Nome, fa.Funcao
FROM TB_Feedback f
JOIN TB_FeedbackAluno faluno 
  ON f.CodFeedback = faluno.CodFeedback
JOIN TB_Aluno a 
  ON faluno.CodAluno = a.Matricula
LEFT JOIN TB_FuncaoAluno fa 
  ON fa.CodAluno = a.Matricula AND fa.CodExt = f.CodExt;
