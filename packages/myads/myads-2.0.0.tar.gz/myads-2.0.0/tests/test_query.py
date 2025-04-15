from myads.query import ADSQueryWrapper

token = "Q9koXzft3H41fFxJCNOVjLExZlJXnLL9VjjYhloK"

query = ADSQueryWrapper(token)

q = "aff:computational cosmology year:2020"
fl = "first_author,title,bibcode,pubdate,citation_count,aff"

data = query.get(q, fl, rows=10)

print(data.papers)
