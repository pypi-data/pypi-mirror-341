
#########################################
# IMPORT Libs
import importlib
import pkgutil
import os

import threading
import asyncio

from openai import OpenAI
import time
import pandas as pd
import shutil
import inspect
import json
import tiktoken
from github import Github
import re
import requests
import base64
from telegram import Bot
import random
from datetime import datetime, timedelta
import struct
from dotenv import load_dotenv, find_dotenv
import git
from requests.auth import HTTPBasicAuth
import sys
import subprocess
import ast
import os
from firebase_admin import credentials, initialize_app, storage, db, delete_app
import platform

import concurrent.futures
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
import pandas as pd
import os

from werkzeug.security import generate_password_hash, check_password_hash

from collections import defaultdict
import sys

import discord
import sys
from discord.ext import commands

import os

import platform

import concurrent.futures
import hashlib
import schedule
from typing import Optional, List, Union
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
from flask import Flask, request, jsonify
import hmac
import hashlib

import urllib.parse


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas
## IMPORTS Libs
import sys
import os

from typing import Dict, Any

import psutil

import math
import hashlib
from typing import Dict, Any
import os






import concurrent.futures
from reportlab.platypus import PageBreak
from reportlab.lib.colors import Color, black, white


from reportlab.platypus import Image as Imagereportlab
from reportlab.platypus import PageBreak, Table, TableStyle,Preformatted,  Paragraph, HRFlowable, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Paragraph, PageBreak, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle



import random

import os

from firebase_admin import credentials, storage, db

import firebase_admin
import obsws_python as obs
from openai import OpenAI
import base64

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from termcolor import cprint
from reportlab.platypus import NextPageTemplate

from huggingface_hub import InferenceClient
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from reportlab.pdfgen import canvas


import random
from openai import OpenAI




from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


from firebase_admin import credentials, initialize_app, storage, db

from datetime import datetime, timedelta
from PIL import Image 

import os
import sys


import random


import platform
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any
from collections import defaultdict
from queue import Queue, Empty
import threading

# Bibliotecas de terceiros
try:
    
    import shutil
    import whisper
    import glob
    import math
    import torch
    import traceback
    import hashlib
    from concurrent.futures import ThreadPoolExecutor
    import uiautomator2 as u2
    import cv2
    import numpy as np
    import wave
    import srt
    import yt_dlp
    import psutil
    import schedule
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    

    import websockets
    import asyncio
    import av
    import logging
    import io


    from dotenv import load_dotenv, find_dotenv
    
    from transformers import (
        AutoModelForSpeechSeq2Seq,
        AutoTokenizer,
        AutoFeatureExtractor,
        pipeline,
    )

    from proglog import ProgressBarLogger
except ImportError as e:
    print(f"Erro ao importar bibliotecas: {e}")
    
#########################################
