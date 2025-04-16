import stash

d = {}
db = stash.PyDB(d)

a = 3
m = [1, 2, 3]
l = [m, 2, m]

b = db.dumps(l)

print(d)
v, = d.values()
n = 2 + v[1]
print(v[n:])

print(db.loads(b))
