DO
$$
BEGIN
    TRUNCATE TABLE tb_departamento, tb_materia, tb_curso, tb_cursodep, tb_aluno,
                   tb_historicoaluno, tb_docente, tb_pessoa, tb_local CASCADE;

    -- Reset sequences
    ALTER SEQUENCE tb_departamento_coddep_seq RESTART WITH 1;
    ALTER SEQUENCE tb_materia_codmateria_seq RESTART WITH 1;
    ALTER SEQUENCE tb_curso_codcurso_seq RESTART WITH 1;
    ALTER SEQUENCE tb_local_codlocal_seq RESTART WITH 1;
    ALTER SEQUENCE tb_feedback_codfeedback_seq RESTART WITH 1;
    -- Add others as needed...
END;
$$;

INSERT INTO tb_departamento (Nome,Sigla) values ('Departamento de Ciência da Computação', 'CIC');
INSERT INTO tb_departamento (Nome,Sigla) values ('Departamento de Engenharia Elétrica', 'ENE');
INSERT INTO tb_departamento (Nome,Sigla) values ('Departamento de Matemática', 'MAT');
INSERT INTO tb_departamento (Nome,Sigla) values ('Departamento de Sociologia', 'SOL');
INSERT INTO tb_departamento (Nome,Sigla) values ('Departamento de Linguística, Português, Línguas Clássicas', 'LIP');

INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Introdução aos Sistemas Computacionais','CIC0003');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Algorítmos e Programação de Computadores','CIC0004');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Fundamentos Teóricos da Computação','CIC0002');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Estruturas de dados','CIC0090');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Circuitos Lógicos','CIC0229');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (1, 'Laboratorio de Circuitos Lógicos','CIC0231');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (2, 'Sistemas Digitais','ENE0039');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (2, 'Laboratorio de Sistemas Digitais','ENE0040');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (2, 'Introdução a Circuitos Elétricos','ENE0066');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (2, 'Sinais e Sistemas em Tempo Contínuo','ENE0067');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (3, 'Cálculo 1','MAT0025');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (3, 'Cálculo 2','MAT0026');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (3, 'Cálculo 3','MAT0027');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (3, 'Introdução a Álgebra Linear','MAT0031');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (4, 'Introdução a Sociologia','SOL0042');
INSERT INTO tb_materia (CodDep, Nome, Sigla) values (5, 'Língua de Sinais Brasileira','LIP0174');

INSERT INTO tb_curso (Nome) values ('Ciências da Computação - Bacharelado');
INSERT INTO tb_curso (Nome) values ('Computação - Licenciatura');
INSERT INTO tb_curso (Nome) values ('Engenharia da Computação');
INSERT INTO tb_curso (Nome) values ('Engenharia Elétrica');
INSERT INTO tb_curso (Nome) values ('Matemática - Licenciatura');
INSERT INTO tb_curso (Nome) values ('Matemática - Bacharelado');

INSERT INTO tb_cursodep (codcurso, coddep) values (1, 1);
INSERT INTO tb_cursodep (codcurso, coddep) values (2, 1);
INSERT INTO tb_cursodep (codcurso, coddep) values (3, 1);
INSERT INTO tb_cursodep (codcurso, coddep) values (3, 2);
INSERT INTO tb_cursodep (codcurso, coddep) values (4, 2);
INSERT INTO tb_cursodep (codcurso, coddep) values (5, 3);
INSERT INTO tb_cursodep (codcurso, coddep) values (6, 3);

INSERT INTO tb_aluno (matricula, CodCurso, Nome, CPF, senha, ira, dataingresso, semestreatual)
values ('241003987', 1, 'Luiz Eduardo', '08516392082', 'senhaSegura', 5, '2024-03-10', 3);
INSERT INTO tb_aluno (matricula, CodCurso, Nome, CPF, senha, ira, dataingresso, semestreatual)
values ('221013456', 3, 'Marcos Antônio', '03456769832', 'soualuno', 3.9786, '2022-02-12', 7);
INSERT INTO tb_aluno (matricula, CodCurso, Nome, CPF, senha, ira, dataingresso, semestreatual)
values ('231007522', 1, 'José Costa', '52487608013', 'senhaJose', 4.78, '2023-03-23', 5);
INSERT INTO tb_aluno (matricula, CodCurso, Nome, CPF, senha, ira, dataingresso, semestreatual)
values ('241017449', 1, 'Elisa Souza', '14665612030', 'elisa123', 4.312, '2024-03-10', 3);
INSERT INTO tb_aluno (matricula, CodCurso, Nome, CPF, senha, ira, dataingresso, semestreatual)
values ('221007439', 2, 'Sérgio Ramos', '34992437095', '1234', 3.958, '2022-02-12', 7);

INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('241003987', '241003987@aluno.unb.br');
INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('241003987', 'luizeduardo@gmail.com');
INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('231007522', '231007522@aluno.unb.br');
INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('221013456', '221013456@aluno.unb.br');
INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('241017449', '241017449@aluno.unb.br');
INSERT INTO TB_EmailAluno (codaluno,email) VALUES ('221007439', '221007439@aluno.unb.br');

INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 1, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 2, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 11, 1, 'MS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 3, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 4, 2, 'MS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 5, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('231007522', 6, 2, 'MM');

INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 1, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 2, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 11, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 3, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 4, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 5, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 6, 2, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241003987', 16, 2, 'SS');

INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('221013456', 11, 1, 'MS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('221013456', 12, 2, 'SS');

INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241017449', 4, 1, 'SS');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('241017449', 1, 2, 'MM');

INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('221007439', 2, 1, 'MI');
INSERT INTO tb_historicoaluno (codaluno, codmateria, semestre, mencao)
values ('221007439', 3, 2, 'SS');


INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678900', 2, 'Professor Exemplo', 'senhaProfessor', '11418924059');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678901', 1, 'Maristela Terto de Holanda', 'senhaMaristela', '27638808002');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678910', 1, 'Alba Cristina Magalhaes Alves de Melo', 'senhaAlba', '82484732015');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678911', 1, 'Carla Cavalcante Koike', 'senhaKoike', '01731731019');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678912', 1, 'Daniel de Paula Porto', 'senhaDaniel', '28857711005');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678913', 1, 'Li Weigang', 'senhaLi', '47708906059');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678914', 1, 'Marcus Vinicius Lamar', 'senhaLamar', '59375191087');
INSERT INTO tb_docente (matricula, CodDep, Nome, senha, cpf)
values ('12345678915', 1, 'Edson Ishikawa', 'senhaEdson', '97292835082');

INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678900', 'professor@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678900', 'exemplo@gmail.com');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678901', 'mholanda@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678910', 'alves@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678911', 'ckoike@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678912', 'daniel.porto@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678913', 'weigang@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678914', 'lamar@unb.br');
INSERT INTO TB_EmailDocente (CodDocente,email) VALUES ('12345678915', 'ishikawa@unb.br');

INSERT INTO tb_pessoa (cpf, Nome, senha)
values ('03456978012', 'Ronaldo Pessoa', 'soupessoa');
INSERT INTO tb_pessoa (cpf, Nome, senha)
values ('12888317060', 'Fernando Pessoa', 'soufernando');
INSERT INTO tb_pessoa (cpf, Nome, senha)
values ('17273936006', 'Homo Sapiens', 'sousapiens');
INSERT INTO tb_pessoa (cpf, Nome, senha)
values ('12908924072', 'Manuel Homem Pessoa', 'souhumano');
INSERT INTO tb_pessoa (cpf, Nome, senha)
values ('62493605063', 'Augusto', 'augustusceasarXXVIIac');

INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('03456978012', 'pessoa@gmail.com');
INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('03456978012', 'ronaldo@gmail.com');
INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('12888317060', 'fpessoa@gmail.com');
INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('17273936006', 'sapiens@gmail.com');
INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('12908924072', 'manuel@gmail.com');
INSERT INTO TB_EmailPessoa (CodPessoa,email) VALUES ('62493605063', 'xxciiac@yahoo.com');

INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('FT-Unb', 'Campus','DF','Brasília','Asa Norte');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('CEMI Cruzeiro', 'Outro','DF','Brasília','Cruzeiro');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('CIC-Unb', 'Campus','DF','Brasília','Asa Norte');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('LINF', 'Campus','DF','Brasília','Asa Norte');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('Laboratório 2 do CEMI Cruzeiro', 'Outro','DF','Brasília','Cruzeiro Velho');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro, complemento) VALUES ('Escola Classe 411 Norte', 'Escola','DF','Brasília','Asa Norte', 'SQN 411');
INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) VALUES ('Escolas Públicas do DF', 'Escola','DF','Brasília','-');

CALL insert_extensao(4, 'IV Maratona APC de Programação', 'Evento', 'Oferecer uma atividade de programação competitiva aos estudantes da Universidade de Brasília, focando no nível iniciante (conteúdo contemplado na disciplina Algoritmos e Programação de Computadores), para que possam testar seus conhecimentos e ter contato com as competições de programação. A atividade também serve de treino para os estudantes que estão participando da Maratona SBC de Programação e da Olimpíada Brasileira de Informática 2025.',
    'Tecnologia e Produção', 40, 20, 'Discentes de qualquer turma da disciplina Algoritmos e Programação de Computadores', 'Discentes interessados em programação do Ensino Médio das Instituições Públicas e Privadas do Distrito Federal', '2025-07-05' , '2025-07-05', null, null); /*EV001-2024 - daniel*/
CALL insert_extensao(4, 'VI Maratona UnBalloon de Programação', 'Evento', 'Oferecer uma atividade de programação competitiva aos estudantes da Universidade de Brasília, de iniciantes a experientes, para que possam testar seus conhecimentos e ter contato com as competições de programação. A atividade também serve de treino para os estudantes que estão participando da Maratona SBC de Programação e da Olimpíada Brasileira de Informática 2025.',
    'Tecnologia e Produção', 40, 20, 'Alunos dos cursos de computação', 'Alunos dos cursos de computação de outras universidades do DF', '2025-05-17' , '2025-05-17', '2024-12-10', null); /*EV001-2025 - daniel*/
CALL insert_extensao(3, 'Meninas.comp nas Escolas', 'Curso', 'Curso de meninas da área de ciências da computação para escolas.',
    'Educação', 20, 400, 'Alunos de Graduação da área de Computação e Engenharia', 'Alunas de Escolas de Ensino Médio e Fundamental', '2025-05-17' , '2025-05-17', '2025-03-18', '11:16:00 ');  /*CR001-2025 - koike*/
CALL insert_extensao(7, 'Meninas.comp: Computação também é coisa de meninas!', 'Projeto', 'As mulheres na Computaçãotem uma baixa representatividade em cursos de graduação no Brasil, realidade semelhante a outros paises do mundo. No Brasil, nos anos 2000 e 2013, o de concluintes dos cursos de computação do genero masculino aumentou 98%, enquanto o numero de concluintes do genero feminino diminuiu 8%. Na Universidade de Brasilia o numero de meninas ingressantes do Departamento de Ciência da Computação na graduacao em 2019, que foi inferior a 20%. O Departamento de Ciência da Computação tem 4 cursos: Licenciatura em Computação. Ciência da Computação, Engenharia de Computação e Engenharia Mecatrônica. Com o intuito de incentivar mais meninas a seguirem carreira de Computação essa ação tem como objetivo ensinar programação para as meninas de escolas públicas do ensino médio do Distrito Federal.',
    'Educação', 200, 1000, 'Alunas do curso de Computação da UnB', 'Alunas de escola pública do DF', '2025-04-01' , '2025-12-31', '2025-02-28', '17:29:32'); /*PJ001-2025 - maristela*/
CALL insert_extensao(1, 'Meninas.comp: Robótica também é coisa de menina!', 'Projeto', 'São objetivos deste projeto: 1) Fornecer informação sobre a atuação profissional nas áreas de computação e engenharia; 2) Incentivar a reflexão sobre a pouca atuação da mulher nas áreas de computação e engenharia; 3) Promover a experimentação com Robótica, apresentando sua relação com a atuação da profissional nas áreas de computação e engenharia. 4) Desenvolvimento de projetos integrados da Universidade com os ensinos fundamental e médio. ',
    'Educação', 100, 200, 'Discentes dos cursos de Ciencia da Computação, Engenharia de Computação e Engenharia Mecatrônica', 'Discentes de Escola Pública dos anos finais do Ensino Fundamental e do Ensino Médio', '2025-04-01' , '2025-12-31', null, null);  /*PJ002-2025 - koike*/
CALL insert_extensao(1, 'Curso de Introdução ao Hacking Ético', 'Evento', 'O curso de Hacking Ético tem como objetivo introduzir os alunos aos conceitos fundamentais da segurança da informação, apresentando práticas e ferramentas usadas para proteger sistemas e dados de forma responsável e ética. O curso combina teoria e atividades práticas dinâmicas, desenvolvidas especialmente para estimular o pensamento crítico, a responsabilidade digital e o interesse pela tecnologia de forma segura e consciente.',
    'Educação', 10, 10, 'Alunos da Licenciatura em Computação', 'Alunos e professores do CEMI Cruzeiro', '2025-06-24' , '2025-12-5', null, null); /*EV002-2025 -EDISON ISHIKAWA*/


INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-05','08:19:16','PJ001-2025','AGUARDANDO APROVAÇÃO DOS DEPARTAMENTOS');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-05','12:42:27','PJ001-2025','SUBMETIDA');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-06','09:41:52','PJ001-2025','PROPOSTA DEVOLVIDA PARA COORDENADOR REEDITAR');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-06','10:33:08','PJ001-2025','PROPOSTA DEVOLVIDA PARA COORDENADOR REEDITAR');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-06','10:53:28','PJ001-2025','SUBMETIDA');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-03-07','11:38:57','PJ001-2025','AGUARDANDO AVALIAÇÃO');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-05-08','17:03:08','PJ001-2025','APROVADO COM RECURSOS');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-05-08','17:03:38','PJ001-2025','EM EXECUÇÃO');

INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-05-08','16:59:51','CR001-2025','AGUARDANDO APROVAÇÃO DOS DEPARTAMENTOS');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-05-22','14:29:43','CR001-2025','SUBMETIDA');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-06-09','16:19:11','CR001-2025','PROPOSTA DEVOLVIDA PARA COORDENADOR REEDITAR');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-06-10','08:27:33','CR001-2025','PROPOSTA CORRIGIDA E DEVOLVIDA PARA O PRESIDENTE');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-06-11','11:43:29','CR001-2025','PROPOSTA DEVOLVIDA PARA COORDENADOR REEDITAR');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-06-11','11:44:02','CR001-2025','AGUARDANDO AVALIAÇÃO');
INSERT INTO TB_SituacaoExt (DataSit,HorarioSit,codext,Situacao) VALUES ('2025-06-25','18:55:04','CR001-2025','EM EXECUÇÃO');


INSERT INTO TB_FuncaoPessoa(CodPessoa,CodExt,Funcao,EstadoInscricao) VALUES ('62493605063','EV001-2024',null,'Indeferido');
INSERT INTO TB_FuncaoPessoa(CodPessoa,CodExt,Funcao,EstadoInscricao) VALUES ('62493605063','CR001-2025',null,'Indeferido');
INSERT INTO TB_FuncaoPessoa(CodPessoa,CodExt,Funcao,EstadoInscricao) VALUES ('62493605063','PJ002-2025',null,'Em Espera');
INSERT INTO TB_FuncaoPessoa(CodPessoa,CodExt,Funcao,EstadoInscricao) VALUES ('62493605063','PJ001-2025',null,'Indeferido');
INSERT INTO TB_FuncaoPessoa(CodPessoa,CodExt,Funcao,EstadoInscricao) VALUES ('62493605063','EV002-2025','Supervisor(a)','Deferido');

INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('241003987','EV001-2024',null,'Em Espera');
INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('241003987','CR001-2025',null,'Indeferido');
INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('241017449','CR001-2025','Aluno(a) voluntário(a)','Deferido');
INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('241003987','EV001-2025','Aluno(a) bolsita','Deferido');
INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('221007439','EV001-2025',null,'Indeferido');
INSERT INTO TB_FuncaoAluno(CodAluno,CodExt,Funcao,EstadoInscricao) VALUES ('231007522','EV002-2025','Aluno(a) voluntario(a)','Deferido');

INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678912','EV001-2024','Coordenador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678912','EV001-2025','Coordenador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678911','CR001-2025','Coordenador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678901','PJ001-2025','Coordenador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678911','PJ001-2025','Colaborador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678911','PJ002-2025','Coordenador(a)','Deferido');
INSERT INTO TB_FuncaoDocente(CodDocente,CodExt,Funcao,EstadoInscricao) VALUES ('12345678915','EV002-2025','Coordenador(a)','Deferido');


INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV001-2024','Demais esse evento, me diverti bastante',5);        /*1*/
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV001-2025','Gostei, mas achei dificil',4);                      /*2*/        
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV001-2025','Gostei, mas achei fácil',3);                        /*3*/  
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('CR001-2025','Ótima ideia do curso! Vamos fazer mais desses',5);  /*4*/
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('PJ001-2025','Esse trabalho é ótimo!',5);                         /*5*/
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV002-2025','Aprendi bem',4);                                    /*6*/                                    

INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV001-2024','Show!!',5);                                         /*7*/                               
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('CR001-2025','Trabalho incrível',5);                              /*8*/                                          
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('PJ001-2025','Belíssimo trabalho',5);                             /*9*/                                           
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('PJ002-2025','Interessante esse projeto',5);                      /*10*/                                                 
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV002-2025','Bem legal a dinâmica!',5);                          /*11*/   

INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('CR001-2025','Bem joia',5);                                       /*12*/                                 
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('PJ001-2025','Belíssimo trabalho',5);                             /*13*/                                           
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('PJ002-2025','Que legal ver a unb na sociedade',5);               /*14*/                                                         
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV002-2025','Interessante',5);                                   /*15*/                                     
INSERT INTO TB_Feedback(CodExt,Comentario,Nota) VALUES ('EV001-2024','Lorem ipsum',5);                                    /*16*/                                    


INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (1,'241003987');
INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (2,'241003987');
INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (3,'221013456');
INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (4,'231007522');
INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (5,'231007522');
INSERT INTO TB_FeedbackAluno(CodFeedback,CodAluno) VALUES (6,'221007439');

INSERT INTO TB_FeedbackDocente(CodFeedback,CodDocente) VALUES (7,'12345678900');
INSERT INTO TB_FeedbackDocente(CodFeedback,CodDocente) VALUES (8,'12345678900');
INSERT INTO TB_FeedbackDocente(CodFeedback,CodDocente) VALUES (9,'12345678900');
INSERT INTO TB_FeedbackDocente(CodFeedback,CodDocente) VALUES (10,'12345678900');
INSERT INTO TB_FeedbackDocente(CodFeedback,CodDocente) VALUES (11,'12345678900');

INSERT INTO TB_FeedbackPessoa(CodFeedback,CodPessoa) VALUES (12,'03456978012');
INSERT INTO TB_FeedbackPessoa(CodFeedback,CodPessoa) VALUES (13,'12888317060');
INSERT INTO TB_FeedbackPessoa(CodFeedback,CodPessoa) VALUES (14,'12888317060');
INSERT INTO TB_FeedbackPessoa(CodFeedback,CodPessoa) VALUES (15,'12908924072');
INSERT INTO TB_FeedbackPessoa(CodFeedback,CodPessoa) VALUES (16,'62493605063');





SELECT * from tb_departamento;
SELECT * from tb_curso;
SELECT * from tb_materia;
select * from tb_cursodep;
SELECT * from tb_aluno;
select * from tb_docente;
select * from tb_pessoa;
select * from tb_historicoaluno where codaluno = '231018893';
SELECT * from tb_local;
select * from tb_extensao;
select * from tb_situacaoext;

