# Create your views here.
from django.shortcuts import render
import requests

def api(request):
    response = requests.get('http://127.0.0.1:8000/api')
    apidata = response.json()
    out=[]
    for i in apidata:
        for j in i:
            out.append(i[j])
    a = len(out)
    k = a/5
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    for h in range(0,int(a),6):
         data={'title':out[h],
                }
         list1.append(data)
         
    for h in range(1,int(a),6):
         data={
                'location':out[h],
                }
         list2.append(data)
    for h in range(2,int(a),6):
         data={
                'content':out[h],
                }
         list3.append(data)
    for h in range(3,int(a),6):
         data={
                'crimetype':out[h],
                }
         list4.append(data)
    for h in range(4,int(a),6):
         data={
                'state':out[h],
                }
         list5.append(data)
    for h in range(5,int(a),6):
         data={
                'city':out[h],
                }
         list6.append(data)
    
    
         data={'title':list1, 'location':list2, 'content':list3, 'crimetype':list4, 'state':list5, 'city':list6}
         data1={'rest':zip(list2,list4,list5,list6)}
    return render(request, 'api.html', data1)

