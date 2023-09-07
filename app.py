import streamlit as st
from streamlit_option_menu import option_menu
from pytube import YouTube ,Playlist
import requests ,openpyxl
from youtube_transcript_api import YouTubeTranscriptApi

import pandas as pd
import nltk
from collections import Counter
import plotly.express as px
# import winsound
import numpy as np

import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["Add New captions/subtitles","Add New playlist" ,'View Stored Data','Classfy Stored Data'], 
        icons=['Add','gear', 'gear', 'gear'], menu_icon="cast", default_index=0)
if selected == "Add New playlist":
    st.title("Add New playlist")
    url = st.text_input('The YouTube link')
    if st.button('Get playlist'):
        URL_PLAYLIST = url


        playlist = Playlist(URL_PLAYLIST)
        
        st.warning('Number Of Videos In playlist: %s' % len(playlist.video_urls), icon="😺")
        
        for url in playlist:
            print(url)
            key=url.split('/watch?v=')
            if key[0] == 'https://www.youtube.com':
            #    open excel sheet
                workbook = openpyxl.Workbook()
                workbook = openpyxl.load_workbook("example.xlsx")
                worksheet = workbook.active
                
                yt = YouTube(url)
            
                try:
                    srt = YouTubeTranscriptApi.get_transcript(key[1])
                
                    # prints the result
                    tex = ""
                    for t in srt:
                        tex = " "+tex + t['text'].replace('\n', '')
                    
                    column = worksheet["H"]
                    search_value = tex.replace('   ', '')
                    flag = False
                    for cell in column:
                        # Check if the cell contains the search value
                        if cell.value == search_value:
                            # Print the cell address and value
                            flag=True
                    if not flag:
                        worksheet.append([str(yt.author), str(yt.title),str(yt.publish_date),str(yt.length),str(yt.keywords),str(yt.views),str(yt.metadata),tex.replace('   ', '')])
                        workbook.save("example.xlsx")
                        # frequency = 5000  # Set Frequency To 2500 Hertz
                        # duration = 100 # Set Duration To 1000 ms == 1 second
                        # winsound.Beep(frequency, duration)
                
                    else:
                        st.warning('Transcript already exists', icon="⚠️")
                        # frequency = 250  # Set Frequency To 2500 Hertz
                        # duration = 10 # Set Duration To 1000 ms == 1 second
                        # winsound.Beep(frequency, duration)
                except Exception as e :
                    print(e)
                    st.warning('video dose not have Transcript', icon="⚠️")
                    # frequency = 2500  # Set Frequency To 2500 Hertz
                    # duration = 100 # Set Duration To 1000 ms == 1 second
                    # winsound.Beep(frequency, duration)
            else:
                st.warning('Enter a valid URL', icon="⚠️")
        st.warning('Done', icon="⚠️")
        # frequency = 2500  # Set Frequency To 2500 Hertz
        # duration = 1000  # Set Duration To 1000 ms == 1 second
        # winsound.Beep(frequency, duration)
                
            
                
if selected == "Add New captions/subtitles":
    st.title("Add New captions/subtitles")
    
    
    url = st.text_input('The YouTube link')
    if st.button('Get text'):
        key=url.split('/watch?v=')
        if key[0] == 'https://www.youtube.com':
        #    open excel sheet
            workbook = openpyxl.Workbook()
            workbook = openpyxl.load_workbook("example.xlsx")
            worksheet = workbook.active
            
            yt = YouTube(url)
         
            try:
                srt = YouTubeTranscriptApi.get_transcript(key[1])
            
                # prints the result
                tex = ""
                for t in srt:
                    tex = " "+tex + t['text'].replace('\n', '')
                
                column = worksheet["H"]
                search_value = tex.replace('   ', '')
                flag = False
                for cell in column:
                    # Check if the cell contains the search value
                    if cell.value == search_value:
                        # Print the cell address and value
                        flag=True
                if not flag:
                    worksheet.append([str(yt.author), str(yt.title),str(yt.publish_date),str(yt.length),str(yt.keywords),str(yt.views),str(yt.metadata),tex.replace('   ', '')])
                    workbook.save("example.xlsx")
                    st.warning('Transcript stored to excel', icon="😺")
                    st.write("Auther: "+ str(yt.author))
                    st.write("title: "+ str(yt.title))
                    st.write("publish date: " + str(yt.publish_date))
                    st.write("length: " + str(yt.length) +"sec.")
                    st.write("keywords: " + str(yt.keywords))
                    st.write("views: " + str(yt.views))
                    st.write("metadata: " + str(yt.metadata))
                    tex
                    
                    
                    
                else:
                    st.warning('Transcript already exists', icon="⚠️")
            except Exception as e :
                print(e)
                st.warning('video dose not have Transcript', icon="⚠️")
        else:
            st.warning('Enter a valid URL', icon="⚠️")
if selected == "View Stored Data":
    st.title("View Stored Data")
    
    
    exceldf = pd.read_excel('example.xlsx')
    options = st.multiselect(
    'Choose Auther',
    exceldf['auther'].drop_duplicates()
    )
    if options:
        data = exceldf.loc[exceldf['auther'].isin(options)]
        data
        
        dataTile = data
        dataTile
        text = ""
        for i in dataTile['subtitles']:
            text = " " +text+" " +str(i)
        
        if st.button('word analysis'):
            if len(text.split(" ")) >=1:
                stop_words = set(nltk.corpus.stopwords.words('english'))

                def word_freq_generator(text):
                    tokens = nltk.word_tokenize(text.lower())
                    tagged_tokens = nltk.pos_tag(tokens)
                    for token, tag in tagged_tokens:
                        if token not in stop_words and token.isalpha() and 'VB' not in tag:
                            yield token
                df = pd.DataFrame(columns=['word', 'frequence'])
                word_freq = Counter(word_freq_generator(text))
                for i in word_freq.items():
                    df = df.append({'word': i[0], 'frequence': i[1]}, ignore_index=True)

                # Create a bar chart
                df

                fig = px.bar(df, x='word', y='frequence')
                st.plotly_chart(fig, theme="streamlit")
            else:
                st.warning('Did not have Transcript', icon="⚠️")
                
if selected == "Classfy Stored Data":
    if st.button("Classfy data", type="primary"):     
        df = pd.read_excel('example.xlsx')
        if df.any:
            # Create a dictionary of rules
            rules = {
                'natural': ['fresh', 'green','leaves','plants','vegetables','fruits','raw','olive oil','preservatives','farm','exquisite'],
                'green': ['organic', 'plant-based', 'basketball'],
                'Environmental': ['harm', 'pollution', 'recycling'],
                'EnvlFriendly': ['friendly package', 'ecology', 'eco-aware','awareness'],
                'Saving': ['cost', 'cheaper','money','less expensive','affordable','at low budget','valuable','alternatives','pocket','financial','discounted','price cut'],
                'StandardOfLiving': ['quality of life', 'matching style','living conditions','lifestyle','busy women','working mother'],
                'Efficiency': ['low waste', 'leftover', 'reuse','storage','seasonal'],
                'HouseholdNeeds': ['basic needs', 'necessity', 'over use','excess demand','shopping essentials','shopping necessary needs','must have'],
                'Health': ['low fats', 'vegan', 'low meat','vitamins','calcium','fibres','easily to digest','bodily friendly','other sources of protein','immunity','wholegrain','gluten-free','sugar free','low sugar'],
                'Quality': ['hygiene', 'balanced', 'well-cooked'],
                'Quantity': ['spoon', 'grams', 'kilos','plates','ingredients','per person','serving','portions','slices','cups'],
                'Diversity': ['varied', 'meet all the tastes', 'family','friends','loved ones','partners','children','multi'],
                'Well-being': ['wellness', 'nutritious', 'energising','refreshing','relaxing'],
                'Tradition': ['traditional dish', 'grandmother dish', 'mother’s dish','iconic','family'],
                'Heritage': ['festivals/Eid', 'events', 'christmas','thanksgiving','ancestors'],
                'Time': ['saving time', 'quick', 'minutes','hours','in no time','fast','instant','busy'],
                'Long-termEffect': ['enduring', 'memorable', 'experiences'],
                'Technology':['cooking','energy saving','gas-saving','smart','cooking utensils','cooking appliances','gadgets'],
                
                
                
                
            }

            df['Categories'] = ''

            # Apply the rules to classify each article
            for index, row in df.iterrows():
                article = row['subtitles']
                categories = []
                
                for category, keywords in rules.items():
                    for keyword in keywords:
                        if keyword in article:
                            categories.append(category)
                            break
                if categories:
                    df.at[index, 'Categories'] = str(categories).replace("[", "").replace("]", "").replace(",", " ") .replace("'", "")
                else:
                    df.at[index, 'Categories'] ="uncategorized"

            # Save the updated DataFrame to a new Excel file
            df.to_excel('classified_vidoes.xlsx', index=False)
            st.warning('classfication 1 done', icon="⚠️")
        df = pd.read_excel('example.xlsx')
        if df.any:
                rules = {
                'natural': ['fresh', 'green','leaves','plants','vegetables','fruits','raw','olive oil','preservatives','farm','exquisite'],
                'green': ['organic', 'plant-based', 'basketball'],
                'Environmental': ['harm', 'pollution', 'recycling'],
                'EnvlFriendly': ['friendly package', 'ecology', 'eco-aware','awareness'],
                'Saving': ['cost', 'cheaper','money','less expensive','affordable','at low budget','valuable','alternatives','pocket','financial','discounted','price cut'],
                'StandardOfLiving': ['quality of life', 'matching style','living conditions','lifestyle','busy women','working mother'],
                'Efficiency': ['low waste', 'leftover', 'reuse','storage','seasonal'],
                'HouseholdNeeds': ['basic needs', 'necessity', 'over use','excess demand','shopping essentials','shopping necessary needs','must have'],
                'Health': ['low fats', 'vegan', 'low meat','vitamins','calcium','fibres','easily to digest','bodily friendly','other sources of protein','immunity','wholegrain','gluten-free','sugar free','low sugar'],
                'Quality': ['hygiene', 'balanced', 'well-cooked'],
                'Quantity': ['spoon', 'grams', 'kilos','plates','ingredients','per person','serving','portions','slices','cups'],
                'Diversity': ['varied', 'meet all the tastes', 'family','friends','loved ones','partners','children','multi'],
                'Well-being': ['wellness', 'nutritious', 'energising','refreshing','relaxing'],
                'Tradition': ['traditional dish', 'grandmother dish', 'mother’s dish','iconic','family'],
                'Heritage': ['festivals/Eid', 'events', 'christmas','thanksgiving','ancestors'],
                'Time': ['saving time', 'quick', 'minutes','hours','in no time','fast','instant','busy'],
                'Long-termEffect': ['enduring', 'memorable', 'experiences'],
                'Technology':['cooking','energy saving','gas-saving','smart','cooking utensils','cooking appliances','gadgets'],
                

                
                }

                # Create a function to classify a text article
                def classify_text(text):
                    for category, keywords in rules.items():
                        for keyword in keywords:
                            if keyword in text:
                                return category
                    return 'uncategorized'

                # Classify the text articles in the excel sheet
                for index, row in df.iterrows():
                    text = row['subtitles']
                    category = classify_text(text)
                    df.loc[index, 'Category'] = category

                # Save the excel sheet
                df.to_excel('vidoes_classified.xlsx')
                st.warning('classfication 2 done', icon="⚠️")
                
                col1, col2 = st.columns(2)
                
                with col1:
                
                    df = pd.read_excel('vidoes_classified.xlsx')

                    # Count the occurrences of each category
                    category_counts = df['Category'].apply(pd.Series).stack().value_counts()

                    # Calculate the ratio for each category
                    category_ratios = category_counts #/ category_counts.sum()

                    # Print the category ratios
                    print(len(category_ratios))
                    # for i in category_ratios:
                    #     print(i)
                    woedLen =(category_counts.sum())
                    oneClass = pd.DataFrame()
                    G =  nx.MultiGraph()
                    G.add_node('Sustainability', size=15, title='Head',color='blue',)
                    for clas in category_ratios.keys():
                        G.add_edge('Sustainability',str(clas))
                        G.add_node(str(clas), size=10, title=str(clas)+" frequency:"+str(category_ratios.loc[clas]),color='green')
                        
                        
                        oneClass = oneClass.append({'Class':str(clas) , 'frequency': int(category_ratios.loc[clas]) , 'ratio': int(category_ratios.loc[clas])/woedLen*100}, ignore_index=True)
                        print(f"{clas}: {category_ratios.loc[clas]}") 
                    
                    
                    
                    
                    drug_net = Network(height='456px', width='456px',directed=True, bgcolor='white', font_color='black')
                    drug_net.from_nx(G)
                    drug_net.repulsion(node_distance=520, central_gravity=1.33,spring_length=110, spring_strength=1.70,damping=5.95,)
                    try:
                            path = 'img'
                            drug_net.save_graph(f'{path}\\pyvis_graph.html')
                            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                        # Save and read graph as HTML file (locally)
                    except:
                            path = 'html_files'
                            drug_net.save_graph(f'{path}\\pyvis_graph.html')
                            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')
                
                    oneClass=oneClass.sort_values(by=['frequency'],ascending=False)
                    figOne = px.bar(oneClass, x='Class', y='frequency',hover_data=['ratio'],color='Class',labels={'pop':'ratio'}, height=400)
                    st.title("classification by one Lable to each video")
                    st.plotly_chart(figOne)
                    components.html(HtmlFile.read(), height=456 ,width=456,scrolling=True)
                    fig = px.treemap(oneClass, path=['Class', 'frequency'],
                        values='frequency',
                        color='Class')
        
                    st.plotly_chart(fig)
                    st.dataframe(oneClass)
                
                with col2:
                    nltk.download('punkt')
                    nltk.download('stopwords')
                    nltk.download('averaged_perceptron_tagger')

                    df = pd.read_excel('classified_vidoes.xlsx')
                    text = ""
                    for i in df['Categories']:
                        text = " " +text+" " +str(i)
                        
                    tokens = nltk.word_tokenize(text)

                    # Create a dictionary to store the word frequencies.
                    word_frequencies = {}
                    woedLen =len(tokens)
                    # Iterate over the tokens.
                    for token in tokens:
                        # Increment the word frequency.
                        if token in word_frequencies:
                            word_frequencies[token] += 1
                        else:
                            word_frequencies[token] = 1

                    # Print the word frequencies.
                    multiClass = pd.DataFrame()
                    G =  nx.MultiGraph()
                    G.add_node('Sustainability', size=15, title='Head',color='blue',)
                    print(len(word_frequencies.items()))
                    for word, frequency in word_frequencies.items():
                        G.add_edge('Sustainability',str(word))
                        G.add_node(str(word), size=10, title=str(word) +" frequency:"+str(frequency),color='green')
                        
                        multiClass = multiClass.append({'Class':str(word) , 'frequency': int(frequency) , 'ratio':int(frequency)/woedLen*100 }, ignore_index=True)
                        print(f"{word}: {frequency}")  
                        
                    drug_net = Network(height='456px', width='456px',directed=True, bgcolor='white', font_color='black')
                    drug_net.from_nx(G)
                    drug_net.repulsion(node_distance=520, central_gravity=1.33,spring_length=110, spring_strength=1.70,damping=5.95,)
                    try:
                            path = 'img'
                            drug_net.save_graph(f'{path}\\pyvis_graph.html')
                            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                        # Save and read graph as HTML file (locally)
                    except:
                            path = 'html_files'
                            drug_net.save_graph(f'{path}\\pyvis_graph.html')
                            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')
                    
                    
                    multiClass=multiClass.sort_values(by=['frequency'],ascending=False)
                    figMulti = px.bar(multiClass, x='Class', y='frequency',hover_data=['ratio'],color='Class',labels={'pop':'ratio'}, height=400)
               
                    st.title("classification by many Lables to each video")
                    st.plotly_chart(figMulti)
                    components.html(HtmlFile.read(), height=456 ,width=456,scrolling=True)
                    fig = px.treemap(multiClass, path=['Class', 'frequency'],
                        values='frequency',
                        color='Class')
        
                    st.plotly_chart(fig)
                    st.dataframe(multiClass)
                
                    
                
        
