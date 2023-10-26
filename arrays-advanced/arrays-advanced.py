import copy
import csv

def read_csv(plik):
    data_frame = []
    with open(plik) as f:
        csv_reader = csv.reader(f)
        headings_row = next(csv_reader)
        data_frame.append([headings_row[i] for i in range(len(headings_row))])
        for row in csv.reader(f):
            data_frame.append([int(row[i]) for i in range(len(row))])
    return data_frame

def print_data(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(f"{M[i][j]:^10}", end="")
        print()

def right_join(M1, M2):
    ans=[]
    r_b=[False]*len(M2)
    ind=None
    for i in range(len(M1)):
        right=False
        for j in range(len(M2)):
            if M1[i][0]==M2[j][0]:
                ind=j
                right=True
                break
        if right:
            ans.append(copy.copy(M1[i])+[M2[ind][k] for k in range(1, len(M2[ind]))])
            r_b[ind]=True
    for j in range(len(M2)):
        if not r_b[j]:
            ans.append([M2[j][0]]+[float("NaN")]*(len(M1[0])-1)+[M2[j][k] for k in range(1, len(M2[j]))])
    return ans


def evaluate(M, team, r):
    ans=[]
    for i in range(1, len(M)):
        if M[i][1]==team:
            tmp=[M[i][0], 0]
            for k in range(len(r)):
                tmp[1]+=M[i][2+k]*r[k]
            ans.append(tmp)
    return ans

def best_team(M, teams, r):
    score=0
    best_t=0
    for t in teams:
        data=evaluate(M, t, r)
        sum=0
        for elem in data:
            sum+=elem[1]
        rate=sum/len(data)
        if rate>score:
            score=rate
            best_t=t
    return best_t, score

def main():
    M1, M2=read_csv("m1B.csv"), read_csv("m2B.csv")
    M=right_join(M1, M2)
    print_data(M)
    r = [1, 1.5, 2, -0.5]
    teams = [100, 101, 103, 104, 105]
    best_t, score=best_team(M, teams, r)
    print(f"Zespół {best_t} uzyskał najwyższą średnią ocenę: {score}")

if __name__ == "__main__":
    main()