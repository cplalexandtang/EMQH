from flask import Flask, abort, jsonify
import json
import requests
import re

app = Flask(__name__)
key = ["向量分析", "靜電學", "靜磁學", "馬克斯威爾方程式", "平面波理論", "時域傳輸線", "頻域傳輸線", "波導", "史密斯圖"]
URL = "http://em.emedu.org.tw/exercise/practice/flusher"

@app.route('/emans/<string:img_src>', methods=['GET'])
def ans(img_src):
	with open('EM.json') as json_data:
		all_quesions = json.load(json_data)

	for i in range(0,len(key)):
		for question in all_quesions[key[i]]:
			if(question["q_img"] == img_src):
				question_id = question["question_id"]

	res = (requests.post(URL, data = {"data[question_id]" : question_id})).text
	ans = re.search("\"\w?\"", res).group()
	details = re.search("\w+.(jpg|gif|png|GIF)", res)

	return jsonify({"ans" : ans[1:2], "details" : check_details_and_language(details)})

def check_details_and_language(details):
	if (details == None):
		return 0
	details = details.group()
	lng = ["EN", "CH"]
	for l in lng:
		r = requests.get("http://em.emedu.org.tw/images/" + l + '/' + details)
		if(r.status_code == 200):
			return "http://em.emedu.org.tw/images/" + l + '/' + details

if __name__ == "__main__":
    app.run(host="0.0.0.0")
