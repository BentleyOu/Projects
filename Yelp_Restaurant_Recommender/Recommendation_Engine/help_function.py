def preprocessing(texts):
    
    from nltk.stem import WordNetLemmatizer
    
    lemmatizer = WordNetLemmatizer()

    return [''.join([(lemmatizer.lemmatize(w)) for w in texts])]


def text_transformer_lsa(preprocessed_texts):
    
    import pandas as pd
    Tfidf_vectorizer = pd.read_pickle('Tfidf.pkl')
    lsa = pd.read_pickle('lsa_model.pkl')
    
    vectorized_text = Tfidf_vectorizer.transform(preprocessed_texts)
    
    compressed_vector = lsa.transform(vectorized_text)
    
    return compressed_vector

def text_transformer_nmf(preprocessed_texts):
    
    import pandas as pd
    Tfidf_vectorizer = pd.read_pickle('Tfidf.pkl')
    nmf = pd.read_pickle('nmf_model.pkl')
    
    vectorized_text = Tfidf_vectorizer.transform(preprocessed_texts)
    
    compressed_vector = nmf.transform(vectorized_text)
    
    return compressed_vector


def find_similarity_LSA(search, top_search, location, random = False):
    
    import pandas as pd, numpy as np
    doc_topic_lsa = pd.read_pickle('doc_topic_lsa.pkl')
    
    preprocessed_search = preprocessing(search)
    
    search_vector = text_transformer_lsa(preprocessed_search)
    
    location_res_topic = doc_topic_lsa[doc_topic_lsa['city'] == location].iloc[:,0:10]
    restaurant_topic_array = location_res_topic.values
    restaurant_index = location_res_topic.index
    
   
    cosine_list = []
    
    from sklearn.metrics.pairwise import cosine_similarity
    for restaurant in restaurant_topic_array:
        
        cosine_list.append(cosine_similarity([restaurant,search_vector.reshape(-1)])[1][0])
    
    cosine_array = np.array(cosine_list)
    
    restaurant_sim = pd.DataFrame(cosine_array, 
                                  index = restaurant_index,
                                 columns = ['Similarity']).sort_values(by = 'Similarity', 
                                                                       ascending = False)
    if random == False:
        return restaurant_sim[:top_search]
    else:
        return restaurant_sim[:top_search+20].sample(top_search)


def find_similarity_NMF(search, top_search, location, random = False):
    
    import pandas as pd, numpy as np
    doc_topic_nmf = pd.read_pickle('doc_topic_nmf.pkl')
    
    preprocessed_search = preprocessing(search)

    
    search_vector = text_transformer_nmf(preprocessed_search)
    
    location_res_topic = doc_topic_nmf[doc_topic_nmf['city'] == location].iloc[:,0:10]
    restaurant_topic_array = location_res_topic.values
    restaurant_index = location_res_topic.index
    
    cosine_list = []
    
    from sklearn.metrics.pairwise import cosine_similarity
    for restaurant in restaurant_topic_array:
        
        cosine_list.append(cosine_similarity([restaurant,search_vector.reshape(-1)])[1][0])
    
    cosine_array = np.array(cosine_list)
    
    restaurant_sim = pd.DataFrame(cosine_array, 
                                  index = restaurant_index,
                                 columns = ['Similarity']).sort_values(by = 'Similarity', 
                                                                       ascending = False)
    
    if random == False:
        return restaurant_sim[:top_search]
    else:
        return restaurant_sim[:top_search+20].sample(top_search)

