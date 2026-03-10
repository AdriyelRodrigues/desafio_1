import pandas as pd
import csv

class Aluno:
    def __init__(self,nome,matricula, telefone,email,uffmail,status):
        self.nome = nome
        self.matricula = matricula
        self.telefone = telefone
        self.email = email
        self.uffmail = uffmail
        self.status = status
    
    def tem_direito_a_uffmail(self):
        if self.status == "Ativo" and pd.isna(self.uffmail):#not self.uffmail - Pandas tratou as linhas sem uffmail como NaN
            return True
        else:
            return False


class GeradorEmail:
    def __init__(self):
        self.emails = []

    def imprime_sugestoes(self):
        
        for i in range(len(self.emails)):
            print(f'{i+1}# {self.emails[i]}')
        print("\n")
    

    def sugere_email(self,aluno):
        nome_completo_separado = aluno.nome.lower().split()
        sufixo = "@id.uff.br"
        sugestao1 = (nome_completo_separado[0] + sufixo)
        sugestao2 = (nome_completo_separado[0] + nome_completo_separado[1] + sufixo)
        sugestao3 = (nome_completo_separado[0] + nome_completo_separado[1][0] + sufixo)
        self.emails.append(sugestao1)
        self.emails.append(sugestao2)
        self.emails.append(sugestao3)
        self.emails.append("uffmail@id.uff.br")
        print(f'{nome_completo_separado[0]}, por favor escolha uma das opções abaixo para o seu UFFMail')
        
    
    
         

class Sistema:
    def __init__(self):
        self.alunos = []

    def ler_csv(self,arquivo):

        dataframe = pd.read_csv(arquivo)
        
        return dataframe
    
    def carraga_dados(self,arquivo):
        df = self.ler_csv(arquivo)
        for i, linha in df.iterrows():
            novo_aluno = Aluno(
                linha["nome"],
                linha["matricula"],
                linha["telefone"],
                linha["email"],
                linha["uffmail"],
                linha["status"]
            )
            self.alunos.append(novo_aluno)

    def busca_aluno(self, matricula):
        for aluno in self.alunos:
            if(str(aluno.matricula) == str(matricula)):
                return aluno
        return None
    
    def busca_uffmail(self,uffmail):
        for aluno in self.alunos:
            if aluno.uffmail == uffmail:
                return True
        return False
    
    def escreve_uffmail(self,aluno,arquivo):
        
        df = self.ler_csv(arquivo)
        id = df.index[df["matricula"] == aluno.matricula]
        df.loc[id,"uffmail"] = aluno.uffmail
        df.to_csv(arquivo,index=False)
        print(df)


    
    
    def decide_solicitacao(self,arquivo):
        matricula = str(input("Digite sua matricula\t"))
        gerador = GeradorEmail()

        aluno = self.busca_aluno(matricula)
        if aluno == None:
            print("Voce precisa ter uma matricula para ter um UffMaill")
            return 
        
        if aluno.tem_direito_a_uffmail() == False:
            print("Aluno não atende aos requisitos para ter um uffmail")
            return 
    
        print("Voce esta atendendo aos requisitos")
        email_ja_existe = True
        gerador.sugere_email(aluno)
        while email_ja_existe:

            gerador.imprime_sugestoes()
            opcao = int(input())
            if opcao > 0 and opcao <= len(gerador.emails):
                email_ja_existe = self.busca_uffmail(gerador.emails[opcao-1])
                if email_ja_existe:
                    print("Esse uffmail ja existe")
            else:
                print("Digite uma opcao valida")

        aluno.uffmail = gerador.emails[opcao-1]
        print(f'A criação de seu e-mail {aluno.uffmail} será feita nos próximos minutos.Um SMS foi enviado para {aluno.telefone} com a sua senha de acesso')
        self.escreve_uffmail(aluno,arquivo)
        return 
        
    
   

nome_arq = "alunoscopia.csv"
s = Sistema()
df = s.ler_csv(nome_arq)
s.carraga_dados(nome_arq)
#print(df.loc[df["matricula"] == 100406])
s.decide_solicitacao(nome_arq)

#print(df.loc[:,"status"])

#df = pd.DataFrame()
#df.loc["status"]

#1-Receber o numero da matricula do aluno

#2- Verificar se a matricula esta no csv. Se nao tiver, pedir cadastro do aluno

#3- Tendo a matricula, verificar se o status eh igual a "Ativo"