# importer.py
import tkinter as tk
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
import threading
import pygame
import customtkinter