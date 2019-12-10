import pandas as pd

def auto_Complete(product_name, top_num = 3):

    # text preprocessing
    split_product = ''
    for word in product_name.lower().split():
        split_product += ' '.join([char for char in word]) + ' '

    product_document = split_product[:-1]

    char_vectorizer = pd.read_pickle('char_vectorizer.pkl')
    product_char_array = char_vectorizer.transform([product_document]).todense()

    # find the number of spaces in the product name
    num_space = len(product_name.split()) -1

    # generate the array needed to pass into cosine similarity
    product_array = np.append(np.array(product_char_array).reshape(-1), [[num_space]])

    # create an empty list of cosine similarity values
    cosine_sim_list = []

    product_vect_df = pd.read_pickle('product_vect_df.pkl')

    for array in product_vect_df.values:
        cosine_sim = cosine_similarity([array,product_array.reshape(-1)])[1][0]
        cosine_sim_list.append(cosine_sim)

    cosine_sim_df = pd.DataFrame(np.array(cosine_sim_list),
                                 index = product_vect_df.index,
                                columns = ['Similarity'])

    top_products = cosine_sim_df.sort_values(by = 'Similarity', ascending = False)

    if top_products.iloc[0,0] >= 0.95:
        return top_products.index[0]
    else:
        print('Did you mean one of these?')
        return [item for item in top_products.index[:top_num]]
        print('Try again with these options')


def find_association(item_nameAnt = None, item_nameCon = None, num_association = 3):
    
    '''
    item_nameAnt is the antecedent 
    itemname_Cont is the consequent
    
    RETURN: num_association = 3 (by default)
    
    A tuple of lists corresponding to (ant_assocation, ant_cond, con_assocation, con_cond)
    
    ant_association - the products associated with the antecedent with a lift score > 1 (high to low)
    ant_cond - the products associated with the antecedent with decreasing confidence score
    
    cond_association - the products associated with the consequent with a lift score > 1 (high to low)
    ant_cond - the products associated with the consequent with decreasing confidence score
    
    It is possible that one or more of the outputs contains an empty list
    '''

    rules = pd.read_pickle('rules.pkl')
    association_df_a = rules[rules.itemA == item_nameAnt].sort_values(by = 'confidenceAtoB', ascending = False)
    association_df_c = rules[rules.itemB == item_nameCon].sort_values(by = 'confidenceBtoA', ascending = False)

    # all the prodcuct item which has a lift greater than 1
    association_items = set(list(rules[rules.lift > 1].itemB.unique()) + list(rules[rules.lift > 1].itemA.unique()))

    # check if the Ant item is a association item
    # if so, print the Con items with a lift > 1
    ant_association = []
    if item_nameAnt in association_items:
        print(f'You have found {item_nameAnt} to have high associations with: ')
        high_lift = rules[rules.itemA == item_nameAnt].sort_values(by = 'lift', ascending = False)
        for item in high_lift[high_lift.lift > 1].itemB:
            ant_association.append(item)
            print(item)

    ant_cond = []
    if item_nameAnt != None:
        print('\n\n')
        print(f'If they bought {item_nameAnt}, they will also buy:')
        for index, item in enumerate(association_df_a.iloc[:num_association,1]):
            ant_cond.append(item)
            print(f'{item}, {round(association_df_a.iloc[index,8],3)}')


    # check if the Con item is a association item
    # if so, print the Ant items with a lift > 1
    con_association = []
    if item_nameCon in association_items:
        print('\n\n')
        print(f'You have found {item_nameCon} to have high associations with: ')
        high_lift = rules[rules.itemB == item_nameCon].sort_values(by = 'lift', ascending = False)
        for item in high_lift[high_lift.lift > 1].itemA:
            con_association.append(item)
            print(item)

    con_cond = []
    if item_nameCon != None:
        print('\n\n')
        print(f'These are the products they will buy before purchasing {item_nameCon}:')
        for index, item in enumerate(association_df_c.iloc[:num_association,0]):
            con_cond.append(item)
            print(f'{item}, {round(association_df_c.iloc[index,9],3)}')


    return (ant_association, ant_cond, con_association, con_cond)
