# Description
Sometimes order does not go through on Zaif official site (freezes for a while and returns null).This tool repeats the order request until the order is placed on the board. <br>
Main function <br>
1) Acquire asset and price information <br>
2) Submit buy / sell order <br>
3) Check the status of thrown order <br>
4) Cancel the thrown order

# Requirements
python3.6 or above、Flask、zaif-client

# Installation
git clone https://github.com/soarbear/zaif-order-tool.git<br>
cd zaif_order_tool<br>
sudo pip3 install flask<br>
sudo pip3 install zaif-client<br>
python3 app.py<br>
=> now access http://localhost:5000/ with browser.

# Language
<a href="https://memo.soarcloud.com/zaif-web-%E3%82%AA%E3%83%BC%E3%83%80%E3%83%BC%E3%83%84%E3%83%BC%E3%83%AB/">Explained in Japanese</a>

# Disclaimer
The developer will not be responsible for Any losses made by using or referring to the tool.Understand the risks involved, using or referring to the bot on your own responsibility.このツールの利用は自己責任でお願いします。
