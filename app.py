from flask import Flask,request,jsonify                     # Flask was primarily used to host the app and create the API. The library urllib was 
import urllib.request                                       # used to fetch the HTML from the url https://time.com/ and was taken as a string.
import re                                                   # "re" module was used to manually parse the aforementioned string.
							    




def getTimeStories():

	fp = urllib.request.urlopen("https://time.com/")
	mybytes = fp.read()

	mystr = mybytes.decode("utf8")
	fp.close()
	
# Since the instructions were NOT to use the libraries for directly
# parsing HTML, we use regex module to manually parse the HTML file.
# First we fetch the HTML from the URL as a string and then manipulate
# it to retrieve "links" and "titles" from the 'Latest Stories' section.

	ss = re.findall('Latest Stories(.+)</ol>', mystr, flags = re.DOTALL)

# The above line gets us the chunk of a string that is present between 
# "Latest Stories" and the nearest ending tag of <ol>(list tag).

	
	tt = re.findall('<h2.*?>(.+?)</a></h2>', str(ss), flags = re.DOTALL)
# The above line simplifies those chunks which contain our target elements,
# "link" and "title".



# In order to further refine these strings I have used these following loops and 
# made a separate list for links and titles. Thus parsing the strings and storing 
# them in new lists, new_links and new_titles, respectively.

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
		
# Now finally we combine the above two lists to make one json object. for that,
# we use jsonify to create the desired JSON Object array with the 5 Latest stories.

	a_list= []
	for (i,j) in zip(new_titles,new_links):
		a_dictionary = {"title": i,"link":j }
		dictionary_copy = a_dictionary.copy()
		a_list.append(dictionary_copy)


	return jsonify(a_list)


app = Flask(__name__)
@app.route('/getTimeStories', methods=['GET'])

# Creating the API GET call. 

def api():
  if request.method == 'GET':
      return getTimeStories()
if __name__ == '__main__':
  app.run(debug=True)        
