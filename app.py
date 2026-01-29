import os
import requests
from flask import Flask, render_template, request, jsonify

# API Key'i sistem değişkenlerinden çekiyoruz
API_KEY = os.getenv("FIREBASE_API_KEY") 
