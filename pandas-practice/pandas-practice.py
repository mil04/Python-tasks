"""
Milanna Pahasian
Rozwiązanie pracy domowej nr 5
"""

# 1.) Przygotowanie danych

# a) wykonaj import potrzebnych pakietów
import pandas as pd
import sqlite3

# b) wczytaj ramki danych, na których będziesz dalej pracował
Posts = pd.read_csv("./Posts.csv.gz",
compression = 'gzip')
Users = pd.read_csv("./Users.csv.gz",
compression = 'gzip')
Comments = pd.read_csv("./Comments.csv.gz",
compression = 'gzip')

# c) przygotuj bazę danych zgodnie z instrukcją zamieszczoną w treści pracy domowej
baza = 'przyklad.db' # sciezka dostępu do bazy danych:
conn = sqlite3.connect(baza) # połączenie do bazy danych
Comments.to_sql("Comments", conn) # importujemy ramkę danych do bazy danych
Posts.to_sql("Posts", conn)
Users.to_sql("Users", conn)


# 2.) Wyniki zapytań SQL

################ 1 ################
sql_1 = pd.read_sql_query("""SELECT Location, SUM(UpVotes) as TotalUpVotes
FROM Users
WHERE Location != ''
GROUP BY Location
ORDER BY TotalUpVotes DESC
LIMIT 10""",conn)


################ 2 ################
sql_2 = pd.read_sql_query("""SELECT STRFTIME('%Y', CreationDate) AS Year, STRFTIME('%m', CreationDate) AS Month,
COUNT(*) AS PostsNumber, MAX(Score) AS MaxScore
FROM Posts
WHERE PostTypeId IN (1, 2)
GROUP BY Year, Month
HAVING PostsNumber > 1000
""",conn)


################ 3 ################
sql_3 = pd.read_sql_query("""
SELECT Id, DisplayName, TotalViews
FROM (
SELECT OwnerUserId, SUM(ViewCount) as TotalViews
FROM Posts
WHERE PostTypeId = 1
GROUP BY OwnerUserId
) AS Questions
JOIN Users
ON Users.Id = Questions.OwnerUserId
ORDER BY TotalViews DESC
LIMIT 10
""",conn)


################ 4 ################
sql_4 = pd.read_sql_query("""SELECT DisplayName, QuestionsNumber, AnswersNumber, Location, Reputation, UpVotes, DownVotes
FROM (
SELECT *
FROM (
SELECT COUNT(*) as AnswersNumber, OwnerUserId
FROM Posts
WHERE PostTypeId = 2
GROUP BY OwnerUserId
) AS Answers
JOIN
(
SELECT COUNT(*) as QuestionsNumber, OwnerUserId
FROM Posts
WHERE PostTypeId = 1
GROUP BY OwnerUserId
) AS Questions
ON Answers.OwnerUserId = Questions.OwnerUserId
WHERE AnswersNumber > QuestionsNumber
ORDER BY AnswersNumber DESC
LIMIT 5
) AS PostsCounts
JOIN Users
ON PostsCounts.OwnerUserId = Users.Id""",conn)


################ 5 ################
sql_5 = pd.read_sql_query("""SELECT Title, CommentCount, ViewCount, CommentsTotalScore, DisplayName, Reputation, Location
FROM (
SELECT Posts.OwnerUserId, Posts.Title, Posts.CommentCount, Posts.ViewCount, CmtTotScr.CommentsTotalScore
FROM (
SELECT PostId, SUM(Score) AS CommentsTotalScore
FROM Comments
GROUP BY PostId
) AS CmtTotScr
JOIN Posts ON Posts.Id = CmtTotScr.PostId
WHERE Posts.PostTypeId=1
) AS PostsBestComments
JOIN Users ON PostsBestComments.OwnerUserId = Users.Id
ORDER BY CommentsTotalScore DESC
LIMIT 10""",conn)


# Zapisanie każdej z ramek danych opisujących wyniki zapytań SQL do osobnego pliku pickle.
#for i, df in enumerate([sql_1, sql_2, sql_3, sql_4, sql_5], 1):
#    df.to_pickle(f'sql_{i}.pkl.gz')

# Wczytanie policzonych uprzednio wyników z plików pickle (możesz to zrobić, jeżeli zapytania wykonują się za długo).
#sql_1, sql_2, sql_3, sql_4, sql_5 = [
#    pd.read_pickle(f'sql_{i}.pkl.gz') for i in range(1, 5 + 1)
#]

# 3.) Wyniki zapytań SQL odtworzone przy użyciu metod pakietu Pandas.

# zad. 1
try:
    pandas_1=Users[Users['Location'] != ''].groupby('Location').agg({'UpVotes': 'sum'}).reset_index()\
            .sort_values('UpVotes', ascending=False).head(10).rename(columns={'Location': 'Location', 'UpVotes': 'TotalUpVotes'})\
            .reset_index(drop=True)
        
    #najpierw wybralismy dane gdzie Locaton nie puste, liczymy sumu UpVotes po Location, sortujemy w porzadku
    #malejacym, nazywamy kolumny i usuwamy indeksy

    print (pandas_1.equals(sql_1) )

except Exception as e:
    print("Zad. 1: niepoprawny wynik.")
    print(e)

# zad. 2

try:
    pandas_2=Posts[Posts['PostTypeId'].isin([1, 2])].copy()
    pandas_2.loc[:, 'Year'] = pd.to_datetime(pandas_2['CreationDate']).dt.strftime('%Y')
    pandas_2.loc[:, 'Month'] = pd.to_datetime(pandas_2['CreationDate']).dt.strftime('%m')
    pandas_2=pandas_2.groupby(['Year', 'Month']) \
        .agg(PostsNumber=('PostTypeId', 'count'),
             MaxScore=('Score', 'max')) \
        .reset_index()
    pandas_2 = pandas_2[pandas_2['PostsNumber'] > 1000].reset_index(drop=True)
    
    #tworzymy nowa ramke danych, taka, ze ona zawiera wiersze gdzie 'PostTypeId' jest równa 1 lub 2, potem
    #dodajemy kolumne Year, Month, grupujemy według nich, dodajemy nowe kolumny - zliczone PostTypeId i maximum z Score,
    #na koniec, zostawiamy te dane, gdzie PostsNumber>1000
    
    print (pandas_2.equals(sql_2) )

except Exception as e:
    print("Zad. 2: niepoprawny wynik.")
    print(e)

# zad. 3

try:
    pandas_3 = Posts[Posts['PostTypeId'] == 1].groupby('OwnerUserId') \
        .agg(TotalViews=('ViewCount', 'sum')) \
        .reset_index().merge(Users, left_on='OwnerUserId', right_on='Id')
    pandas_3 = pandas_3[['Id', 'DisplayName', 'TotalViews']].sort_values('TotalViews', ascending=False)\
        .head(10).reset_index(drop=True)
    print (pandas_3.equals(sql_3) )

    #najpierw wybieramy z Posts tylko PostTypeId= 1 i grupujemy po OwnerUserId, potem liczymy sumy ViewCount
    #i lanczymy z Users, zatym wybieramy z wyniku tylko okreslone kolumny, sortujemy

except Exception as e:
    print("Zad. 3: niepoprawny wynik.")
    print(e)



# zad. 4

try:
    ans=Posts[Posts['PostTypeId'] == 2].groupby('OwnerUserId').size().reset_index(name='AnswersNumber')
    que=Posts[Posts['PostTypeId'] == 1].groupby('OwnerUserId').size().reset_index(name='QuestionsNumber')
    pandas_4=pd.merge(ans, que, on='OwnerUserId')
    pandas_4=pandas_4[pandas_4['AnswersNumber'] > pandas_4['QuestionsNumber']]\
        .sort_values('AnswersNumber', ascending=False).head(5).merge(Users, left_on='OwnerUserId', right_on='Id') \
        [['DisplayName', 'QuestionsNumber', 'AnswersNumber', 'Location', 'Reputation', 'UpVotes', 'DownVotes']]\
        .reset_index(drop=True)
        
    #w ans wybieramy dane gdzie PostTypeId==2, grupujemy wedlug OwnerUserId i zliczamy ilosc wystąpien 
    #w que wybieramy dane gdzie PostTypeId==1, grupujemy wedlug OwnerUserId i zliczamy ilosc wystąpien
    #potem laczymy je, filtrujemy, zeby AnswersNumber>QuestionsNumber, sortujemy i zostawiamy 5 wierszy
    #wynik laczymy z Users, wybieramy tylko okreslone kolumny
         
    print (pandas_4.equals(sql_4) )

except Exception as e:
    print("Zad. 4: niepoprawny wynik.")
    print(e)


# zad. 5

try:

    cts=Comments.groupby('PostId') \
        .agg(CommentsTotalScore=('Score', 'sum')) \
        .reset_index()[['CommentsTotalScore', 'PostId']]
    pbc=Posts[Posts['PostTypeId'] == 1].merge(cts, left_on="Id", right_on="PostId")\
        [['OwnerUserId','Title','CommentCount','ViewCount','CommentsTotalScore']]
    pandas_5=pbc.merge(Users, left_on='OwnerUserId', right_on='Id').sort_values('CommentsTotalScore', ascending=False)\
        .head(10)[['Title','CommentCount','ViewCount','CommentsTotalScore','DisplayName','Reputation','Location']].reset_index(drop=True)

    #tworzac CmtTotScr grupujemy Comments, tworzymy kolumne sumujac Score i zostawiamy okreslone kolumny
    #w PostsBestComments wybieramy dane z Posts gdzie PostTypeId= 1 i laczymy z CmtTotScr, zostawiamy 5 kolumn
    #wynik laczymy z Users, sortujemy, wybieramy poterzebne kolumny

    print(pandas_5.equals(sql_5))

except Exception as e:
    print("Zad. 5: niepoprawny wynik.")
    print(e)



conn.close()
