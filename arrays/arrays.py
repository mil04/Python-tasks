import math

def mix_with_inversion(arr):
    list=[0]*len(arr)
    for i in range(len(arr)):
        list[i]=arr[i]
    for i in range(len(arr)):
        if i%2==0:
            arr[i]=list[len(arr)-1-i//2]
        else:
            arr[i]=list[(i-1)//2]

def number_to_letter(number):
    return chr(number + ord('a'))

def letter_to_number(letter):
    return ord(letter) - ord('a')

def find_first_letter_occurrence(arr, occurrence_count):
    list=[0]*26
    for i in range(len(arr)):
        number=letter_to_number(arr[i])
        list[number]+=1
        if list[number] == occurrence_count:
            return number_to_letter(number)
    return None

def get_dominators_from_right(arr):
    length=0
    sum=0
    for i in range(len(arr)):
        sum+=arr[i]
    sum_arr=sum
    for i in range(len(arr)-1):
        sum-=arr[i]
        if sum<arr[i]:
            length+=1
    ans=[(0,0,0)]*length
    iter=0
    for i in range(len(arr)-1):
        sum_arr-=arr[i]
        if sum_arr < arr[i]:
            ans[iter]=arr[i],i,sum_arr
            iter+=1
    return ans

def get_digit_by_index(number, index_from_left, invalid_result=-1):
    if index_from_left < 0:
        return invalid_result
    if number == 0 and index_from_left > 0:
        return invalid_result
    if number == 0:
        return 0
    digits_count = int(math.log10(number)) + 1
    if index_from_left + 1 > digits_count:
        return invalid_result
    return number // 10**(digits_count-1-index_from_left) % 10

def join_for_max_number(arr):
    for j in range(len(arr)-1):
        max=arr[j]
        ind=j
        for i in range(j+1,len(arr)):
            if get_digit_by_index(arr[i], 0) > get_digit_by_index(max,0):
                max=arr[i]
                ind=i
            elif get_digit_by_index(arr[i], 0) == get_digit_by_index(max,0):
                if arr[i]<max:
                    max=arr[i]
                    ind=i
                else:
                    continue
            else:
                continue
        arr[j],arr[ind]=arr[ind],arr[j]

def main():
    arr1=[1,2,3,4,5,6]
    mix_with_inversion(arr1)
    print(arr1)
    arr2=[1,2,3,4,5,6,7,8,9]
    mix_with_inversion(arr2)
    print(arr2)
    arr3=['z', 's', 'a', 'z', 't', 'd', 'z', 'a', 'u', 'a', 'a', 't', 'a','z', 'z', 'c', 'q', 'c', 'x', 's', 'z', 'e', 'a', 'q', 'a', 'k', 'a', 'd', 'o', 'a']
    print(find_first_letter_occurrence(arr3,4))
    arr4=['a', 'b', 'c']
    print(find_first_letter_occurrence(arr4, 2))
    print( get_dominators_from_right([1, 9, 0, 4, 1, 2]))
    print( get_dominators_from_right([1, 2, 3, 4, 5, 6]))
    arr5=[11, 2, 8, 99, 22, 0]
    join_for_max_number(arr5)
    print(arr5)
    arr6=[15, 5, 9, 51, 83, 4, 837, 0]
    join_for_max_number(arr6)
    print(arr6)
    pass

if __name__=="__main__":
    main()