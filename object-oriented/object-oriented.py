import random

class AppleTree:
    __slots__=["fruits", "water_level", "is_live"]

    def __init__(self, initial_water_level=1):
        self.fruits=0
        self.water_level=initial_water_level
        self.is_live=True

    def next_day(self, rain_level):
        if self.is_live==True:
            self.water_level-=1
            self.water_level+=rain_level
            if self.water_level>0:
                self.fruits+=1
                self.water_level-=1
            elif self.water_level<0:
                self.fruits=0
                self.is_live=False

    def __str__(self):
        if not self.is_live:
            return 'X'
        return f'{self.fruits}'

class Orchard:
    __slots__=['size', 'field']

    def __init__(self, size):
        self.field=[[None]*size for i in range(size)]
        self.size=size
        number=int(0.2*size*size)
        for i in range(number):
            x=random.randint(0,size-1)
            y=random.randint(0,size-1)
            while not(self.field[x][y] is None):
                x=random.randint(0, size-1)
                y=random.randint(0, size-1)
            water=random.randint(1,3)
            self.field[x][y]=AppleTree(water)

    def __str__(self):
        field_printing=''
        for j in range(len(self.field[0])*2 + 2):
            field_printing+="-"
        field_printing+='\n'
        for i in range(len(self.field)):
            field_printing+="|"
            for j in range(len(self.field[i])):
                if self.field[i][j] is not None:
                    value=f'{self.field[i][j]}'
                    field_printing+=f'{value:>2s}'
                else:
                    field_printing+="  "
            field_printing+="|\n"
        for j in range(len(self.field[0]) * 2 + 2):
            field_printing+='-'
        return field_printing
    def is_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if not(self.field[i][j] is None):
                    if self.field[i][j].is_live==True:
                        return False
        return True

    def create_storm_matrix(self):
        matrix=[[None]*self.size for i in range(self.size)]
        a=random.randint(1,3)
        k=2*a
        for i in range(self.size):
            for j in range(self.size):
                if i>j:
                    matrix[i][j]=random.randint(0,k)
                else:
                    matrix[i][j]=random.randint(0, k//2)
        for i in range(k//2):
            x=random.randint(0, self.size-1)
            y=random.randint(0, self.size-1)
            while matrix[x][y]==-float('Inf'):
                x=random.randint(0, self.size-1)
                y=random.randint(0, self.size-1)
            matrix[x][y]=-float('Inf')
        return matrix

    def next_day(self):
        matrix=self.create_storm_matrix()
        for i in range(self.size):
            for j in range(self.size):
                if not(self.field[i][j] is None):
                    if self.field[i][j].is_live==True:
                        if matrix[i][j]==-float('Inf'):
                            self.field[i][j].fruits=0
                            self.field[i][j].is_live=False
                        else:
                            self.field[i][j].next_day(matrix[i][j])

def main():
    random.seed(2023)
    size=int(input("Please provide orchard size:"))
    O1=Orchard(size)
    print("After planting:")
    print(O1)
    i=1
    while i<=20:
        if O1.is_over():
            i=22
            break
        O1.next_day()
        print(f"Day:{i}")
        print(O1)
        i+=1
    pass

if __name__ == "__main__":
    main()