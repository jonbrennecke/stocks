import urllib 

# TODO: better error code descriptions
class ConnectionError(Exception) :
	def __init__(self,code) :
		self.code = code
		self.msgs = {
			"E001" : "Bad connection",
			"E002" : "Missing data"
		}

	def __str__(self) :
		try :
			return self.msgs[self.code]
		except KeyError:
			return self.msgs["E001"]

# grab a historical stock quote from yahoo api
# @param: 'symbol' <string> of stock ticker symbol
# @param: 'f' <tuple> of day, month, year (starting date)
# @param: 't' <tuple> of day, month, year (ending date)
# @param: 'period' <string> of trading period: daily = d, weekly = w, monthly = m
def historical_quote(symbol,date_from,date_to,period) :
	try :
		a,b,c = map(str,date_from)
		d,e,f = map(str,date_to)
		baseUrl = "http://ichart.yahoo.com/table.csv?s="
		query = baseUrl+symbol+'&a='+a+'&b='+b+'&c='+c+'&d='+d+'&e='+e+'&f='+f+'&g='+period
		content = urllib.urlopen(query)
		p1,p2 = content.read().split("\n")[0:-1]
		p1 = p1.split(",")
		p1.extend(p2.split(","))
		info = {}
		index = None
		for i in range(0,len(p1)) :
			try:
				f = float(p1[i])
				if not index : index = i
				info[p1[i - index+1]] = p1[i]
			except ValueError:
				pass
		info[p1[0]] = p1[index-1]
		return info

	except (ValueError, IOError) as e :
		raise ConnectionError("E001")

# grab a current stock quote from yahoo api
def current_quote(symbol,*tags) :
	baseUrl = "http://download.finance.yahoo.com/d/quotes.csv?s="
	query = baseUrl+symbol+"&f="+tags[0]
	content = urllib.urlopen(query)
	return content.read()

if __name__ == '__main__':

	# stock ticker symbols in the Dow Jones Index (^DJI)
	dji = ["AA","AXP","BA","BAC","CAT","CSCO","CVX","DD","DIS","GE","HD","HPQ","IBM","INTC","JNJ","JPM","KO","MCD","MMM","MRK","MSFT","PFE","PG","T","TRV","UNH","UTX","VZ","WMT","XOM"]

	for stock in dji :
		try :
			print current_quote(stock,'nl1')
			print historical_quote(stock,(2,3,2000),(2,5,2000),'d')
		except ConnectionError :
			pass
