def odd(x):
	return x % 2
	
temp=range(10)
print temp
show=filter(odd,temp)
print show
print list(show)

print 'list view'
print list(filter(lambda x : x % 2, range(10)))

print 'second view'
print list(map(lambda x : x * 2, range(10)))
	