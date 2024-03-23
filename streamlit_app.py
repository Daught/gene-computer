import asyncio
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

def calcOccurence(charTotalCount, gcContentCount):
    return (gcContentCount / charTotalCount) * 100

def count_characters_in_string(string):
    return sum([len(word) for word in string.split()])

async def countGcContent(sequence, charTotalCount, gcContentCount):
    targetCharG = 'G'
    targetCharC = 'C'
    gcContentCount += sequence.count(targetCharC)
    gcContentCount += sequence.count(targetCharG)    
    charTotalCount += count_characters_in_string(sequence)
    return charTotalCount, gcContentCount

def computeSequence(cd28FileName):
    first = True
    gcContentCount = 0
    charTotalCount = 0
    
    for line in cd28FileName:
        line = line.decode("utf-8").rstrip('\n')        
        line = line.upper()
        if line.startswith('>'):
            if not first:
                # show percentage of current sequence            
                st.info(calcOccurence(charTotalCount, gcContentCount))
                charTotalCount = 0 # reset counter(s)
                gcContentCount = 0
            st.write(str(line))  # print sequence-header            
            first = False
        else:
            charTotalCount, gcContentCount = asyncio.run(countGcContent(line, charTotalCount, gcContentCount))
    
    # show percentage of last sequence    
    st.info(calcOccurence(charTotalCount, gcContentCount))    



# Page
st.set_page_config(page_title='GC-Content')
st.title('GC-Content')

# Text Calculator
sequence_from_text_area = st.text_area('Upload a sequence in fasta format', height=300)    
if st.button('Calculate'):    
    charTotalCount = 0
    gcContentCount = 0    
    charTotalCount, gcContentCount = asyncio.run(countGcContent(sequence_from_text_area, charTotalCount, gcContentCount))    
    st.info(calcOccurence(charTotalCount, gcContentCount))

# File Calculator
cd28FileName = st.file_uploader('Choose a file')
if cd28FileName is not None:    
    computeSequence(cd28FileName)
