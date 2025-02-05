import datetime
import time
import inspect
import streamlit as st
import numpy as np

def get_caller_name():
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the caller frame
    caller_frame = current_frame.f_back.f_back.f_back
    # Get the name of the caller function
    caller_name = caller_frame.f_globals['__name__']
    return caller_name
def get_caller_line_number():
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the caller frame
    caller_frame = current_frame.f_back.f_back
    # Get the line number of the caller
    caller_line_number = caller_frame.f_lineno
    return caller_line_number

@st.cache_data
def get_mots():
    caller_name = get_caller_name()
    t_start = time.time()
    mots_f = []
    mots_m = []
    mots_fm = []

    filename = "./data/nom/fs.txt"
    # with open(filename, encoding='utf-8') as lines:
    #     for mot in lines: 
    #         mots_f.append(mot.replace("\n", ""))
    #         mots_f = sorted(mots_f)

    mots_f = sorted(np.genfromtxt(filename, dtype=str, delimiter='\n'))

    filename = "./data/nom/ms.txt"
    # with open(filename, encoding='utf-8') as lines:
    #     for mot in lines: 
    #         mots_m.append(mot.replace("\n", ""))
    #         mots_m = sorted(mots_m)

    mots_m = sorted(np.genfromtxt(filename, dtype=str, delimiter='\n'))

    mots_epi = sorted(set(mots_f) & set(mots_m))

    mots_fx = sorted(set(mots_f) - set(mots_m))

    mots_mx = sorted(set(mots_m) - set(mots_f))

    mots_fm = sorted(set(mots_f) | set(mots_m))


    print("get_mots appelé à ", 
          datetime.datetime.fromtimestamp(time.time()),
          " en ", time.time()-t_start, " secondes depuis la ligne : ",
            get_caller_line_number())

    return mots_f, mots_m, mots_epi, mots_fx, mots_mx, mots_fm