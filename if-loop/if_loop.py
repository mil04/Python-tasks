def main():
    cx, cy=float(input("Podaj cx: ")), float(input("Podaj cy: "))
    x0, y0=float(input("Podaj x0: ")), float(input("Podaj y0: "))
    width=float(input("Podaj szerokość badanego obszaru: "))
    piksel=int(input("Podaj rozdzielczosc: "))
    iter=int(input("Podaj maksymalną liczbę iteracji dla jednego punktu: "))
    if width<=0 or piksel<=0 or iter<0 or piksel%2==0:
        raise ValueError("Błędne dane!")
    iter_done=0
    print(f"Trajektoria punktu ({x0}, {y0}):")
    x, y=x0, y0
    for k in range(iter):
        x, y=x*x-y*y+cx, 2*x*y+cy
        iter_done+=1
        print(f"({x}, {y})")
        if x*x+y*y>4:
            break
    for j in range(piksel):
        for i in range(piksel):
            x=x0+i*width/(piksel-1)-width/2
            y=y0-j*width/(piksel-1)+width/2
            for k in range(iter):
                x,y=x*x-y*y+cx, 2*x*y+cy
                iter_done+=1
                if x*x+y*y>4:
                    break
            if x*x+y*y<=4:
                print("@",end="")
            else:
                print(" ",end="")
        print("")
    print(f"Program wykonał w sumie {iter_done} iteracji przekształcenia (x,y)<-(x^2 - y^2 + {cx}, 2xy + {cy})")


if __name__ == '__main__':
    main()