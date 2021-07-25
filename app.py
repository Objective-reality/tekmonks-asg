from flask import Flask,request,jsonify                     # Flask was primarily used to host the app and create the API. 
import urllib.request                                       # The library urllib was used to fetch the HTML from the url https://time.com/ and was 
import re                                                   # taken as a string input. "re" module was used to manually parse the aforementioned
							    # string.




def getTimeStories():

	fp = urllib.request.urlopen("https://time.com/")
	mybytes = fp.read()

	mystr = mybytes.decode("utf8")
	fp.close()

	ss = re.findall('Latest Stories(.+)</ol>', mystr, flags = re.DOTALL)
	#print(ss)

	#print(type(ss))
	#print(type(mystr))
	tt = re.findall('<h2.*?>(.+?)</a></h2>', str(ss), flags = re.DOTALL)
	#print(tt)


	link = []
	title = []

	for each_item in tt:
		x = each_item.split("/>")
		for i in range(len(x)):
			if(i/2==0):		
				link.append(x[i])
			else:
				title.append(x[i])

	new_links = []
	for each_link in link:
		new_links.append(each_link.replace("<a href=","https://time.com"))

	new_titles = []
	for each_title in title:
		new_titles.append(each_title.replace("\\",""))

	a_list= []
	for (i,j) in zip(new_titles,new_links):
		a_dictionary = {"title": i,"link":j }
		dictionary_copy = a_dictionary.copy()
		a_list.append(dictionary_copy)


	return jsonify(a_list)


app = Flask(__name__)
@app.route('/getTimeStories', methods=['GET'])

def api():
  if request.method == 'GET':
      return getTimeStories()
if __name__ == '__main__':
  app.run(debug=True)        
