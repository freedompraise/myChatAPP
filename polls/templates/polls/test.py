def timeConversion(s):
    # Write your code here
    split=s.split(':')
    split[0]=int(split[0])
    if split[0]>11:
        split[0]-=12
        split[0]=str(split[0])
        split[0]='0'+split[0]
    if 'PM' in split[2]:
        split[0]=int(split[0])
        split[0]+=12 
    split[0]=str(split[0])
    split[2]=split[2][:2]
    join=':'.join(split)
    return join

print(timeConversion('12:00:00AM'))