import random

def linia(start, koniec):
    start_x, start_y = start
    koniec_x, koniec_y = koniec
    if start_x > koniec_x:
        return [(-x, y) for (x, y) in linia((-start_x, start_y), (-koniec_x, koniec_y))]
    if start_y > koniec_y:
        return [(x, -y) for (x, y) in linia((start_x, -start_y), (koniec_x, -koniec_y))]

    px, py = start_x, start_y

    wynik = [None] * (koniec_x - start_x + koniec_y - start_y + 1)
    wynik[0] = (px, py)
    pozycja = 1

    while px != koniec_x or py != koniec_y:
        if (py - start_y) * (koniec_x - start_x) > (koniec_y - start_y) * (px - start_x) or py == koniec_y:
            px += 1
        else:
            py += 1
        wynik[pozycja] = (px, py)
        pozycja += 1

    return wynik

def narysuj_linie(M, sx, sy, kx, ky):
    for (x,y) in linia((sx,sy), (kx,ky)):
        M[x][y]=True

def macierz_widocznosci(M):
    ans=[[None]*len(M[i]) for i in range(len(M))]
    sx,sy=len(M)//2, len(M[0])//2
    for i in range(len(M)):
        for j in range(len(M[i])):
            list=linia((sx,sy), (i,j))
            see=True
            for k in range(1,len(list)-1):
                if M[list[k][0]][list[k][1]]:
                    see=False
            if not see:
                ans[i][j]='?'
            elif M[i][j]:
                ans[i][j]='#'
            else:
                ans[i][j]=' '
    ans[sx][sy]="X"
    return ans

def wypisz_macierz_logiczna(M):
    for j in range(len(M[0]) + 2):
        print("-", end="")

    print()

    for i in range(len(M) - 1, -1, -1):
        print("|", end="")
        for j in range(len(M[i])):
            if M[i][j]:
                print("#", end="")
            else:
                print(" ", end="")
        print("|")

    for j in range(len(M[0]) + 2):
        print("-", end="")
    print()

def wypisz_macierz_znakow(M):
    for j in range(len(M[0])+2):
        print("-",end="")
    print()
    for i in range(len(M)-1,-1,-1):
        print("|",end="")
        for j in range(len(M[i])):
            print(M[i][j],end="")
        print("|")
    for j in range(len(M[0])+2):
        print("-",end="")
    print()

def main():
    n, m=int(input("Podaj wysokość: ")), int(input("Podaj szerokość: "))
    k=int(input("Podaj liczbę linii: "))
    M=[[False]*m for i in range(n)]
    for i in range(k):
        narysuj_linie(M, random.randint(0, len(M)-1), random.randint(0, len(M[0])-1), random.randint(0, len(M)-1),
                      random.randint(0, len(M[0])-1))
        wypisz_macierz_logiczna(M)
    wypisz_macierz_znakow(macierz_widocznosci(M))

if __name__ == "__main__":
    main()
