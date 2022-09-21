def solution(A, B, P):
    # write your code in Python 3.6
    contact_name = ""
    matching_contacts = [number for number in B if P in number]
    print(matching_contacts)
    if len(matching_contacts) == 0:
        contact_name = "NO CONTACT"
    elif len(matching_contacts) == 1:
        pos_num = B.index(matching_contacts[0])
        contact_name = A[pos_num]
    else:
        pos_num = [B.index(matching_contacts[i]) for i in range(len(matching_contacts))]
        print(pos_num)
        names_contacts = [A[i] for i in pos_num]
        print(names_contacts)
        contact_name = min(names_contacts)

    return contact_name

print(solution(['sander', 'amy', 'ann', 'michael'], ['123456789', '234567890', '789123456', '123123123'], '1'))