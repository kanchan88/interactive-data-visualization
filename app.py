import streamlit as st
import pandas as pd
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np


import plotly.express as px

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	st.title("DATA VISUALIZATION")

	menu = ["Home","Login"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("PUBLIC VIEW")
		data = px.data.iris()
		fig = px.scatter(data, x="sepal_width", y="sepal_length", color="species")
		st.plotly_chart(fig)

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				data = px.data.iris()
				fig = px.scatter(data, x="sepal_width", y="sepal_length", color="species")
				st.plotly_chart(fig)

				df = px.data.tips()
				fig2 = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group")
				st.plotly_chart(fig2)

			else:
				st.warning("Incorrect Username/Password")


if __name__ == '__main__':
	main()
