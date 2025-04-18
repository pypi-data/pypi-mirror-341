# https://github.com/ollama/ollama-python
from ollama import chat, ChatResponse,ResponseError
#from querycraft.SQLException import SQLQueryException

BdD = '''
create table etudiants(
	noetu  varchar(6)      not null,
	nom     varchar(10)     not null,
	prenom  varchar(10)     not null,
	primary key (noetu)) ;

create table matieres(
	codemat        varchar(8)      not null primary key,
	titre           varchar(10),
	responsable     varchar(4),
	diplome         varchar(20));

create table notes(
	noe            varchar(6),
	codemat        varchar(8) ,
	noteex          numeric         check (noteex between 0 and 20),
	notecc          numeric         check (notecc between 0 and 20),
	primary key (noe, codemat),
	CONSTRAINT FK_noe       FOREIGN KEY (noe)       REFERENCES etudiants (noetu),
	CONSTRAINT FK_codemat   FOREIGN KEY (codemat)   REFERENCES matieres (codemat));
'''

sql1 = "select * from etudiants ;"
sql1e = "select * from etudiant ;"
erreur1 = '''
ERROR:  relation "etudiant" does not exist
LIGNE 1 : select * from etudiant;
                        ^
'''

sql2 = "select * from etudiants where noteex = 12;"
sql2e = "select * from etudiants where notex = 12;"
erreur2 = '''
ERROR:  column "notex" does not exist
LIGNE 1 : select * from etudiants where notex = 12;
                                        ^
'''


class LLM():
    def __init__(self, modele="gemma3:1b"):
        self.prompt = str()
        self.modele = modele

    def run(self,erreur,sql_attendu, sql_soumis,sgbd, bd):
        try:
            instruction_contexte = f'''
== Contexte ==
Tu parles en français.
Tu es un assistant pour un élève en informatique qui apprend les fondements des bases de données relationnelles et le langage SQL.
Les élèves cherchent à apprendre SQL. Ils ne peuvent ni créer de tables ni modifier leur structure. 
Ils peuvent uniquement proposer des requêtes du langage de manipulation des données (MLD) en SQL. 
Ils te proposent des erreurs de requêtes SQL, tu es chargé de les aider à comprendre leurs erreurs.
'''

            instruction_sgbd = f'''
== SGBD ==

Le SGBD utilisé est {sgbd}.
        
'''
            instruction_base_de_donnees = f'''
== Description de la base de données ==

{bd}
        
'''
            instruction_systeme = f'''
== Instructions ==

L'élève te propose une erreur SQL, prends le soin de l'expliquer en français.
Réponds en français et uniquement à la question posée. 
Réponds directement, sans faire de préambule, en t'appuyant sur les informations de la description de la base de données et sur l'erreur.
La base de données est bien construite. Les noms des tables et des attributs sont corrects. Toutes les tables ont bien été créées.
S'il y a des erreurs, elles viennent nécessairement de la requête. 
'''

            instruction = instruction_contexte + instruction_sgbd + instruction_base_de_donnees + instruction_systeme
            #print(instruction)

            self.prompt = "Expliquer l'erreur suivante ? \n" + erreur + '\n'

            '''
            stream = chat(
                model='codellama:7b',
                messages=[{'role':'system', 'content': instruction},
                          {'role': 'user', 'content': self.prompt}],
                stream=True,
            )
            for chunk in stream:
                print(chunk['message']['content'], end='', flush=True)
            '''

            response: ChatResponse = chat(model=self.modele,options={"temperature": 0.0}, messages=[
                {'role':'system', 'content': instruction},{
                    'role': 'user',
                    'content': self.prompt,
                },
            ])
            # print(response['message']['content'])
            # or access fields directly from the response object
            return response.message.content + '\n' + f"source : Ollama (https://ollama.com/) avec {self.modele} (https://ollama.com/library/{self.modele})\n"
        except Exception as e:
            return ""

def main():
    #SQLQueryException.set_model("codellama:7b")
    mess = LLM("codellama:7b").run(erreur2, sql2, sql2e, "PostgreSQL", BdD)
    print(mess)


if __name__ == '__main__':
    main()