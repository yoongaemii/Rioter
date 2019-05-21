from RiotAPI import *
import pickle
import time

with open('unq_games.pickle', 'rb') as f:
    unq_games = pickle.load(f)

for i in range(0, 6984):
    
    # save as file for every 100 game detail
    rng = (i*100, (i+1)*100)

    match_detail = {} # dictionary to save game detail
    detail_error = [] # list of broken match id

    # starting requests
    start = time.time() 
    
    for index, match in unq_games[rng[0]:rng[1]]:
        try:
            match_detail[match] = get_match_detail(match)
        except:
            print("Match No.{} Broken".format(str(index)))
            detail_error.append(match)
    
    # requests completed
    end = time.time() 
    delta = (end - start)/60
    print("======= {0}th 100 Matches Completed: took {1} minutes =====".format(str(i), str(delta))
    
    # save as pickle
    fn = "match_detail"+str(rng[0])+"_"+str(rng[1])+".pickle"
    with open(fn, 'wb') as f:
        pickle.dump(match_detail, f)

    fn = "detail_error"+str(rng[0])+"_"+str(rng[1])+".pickle"
    with open(fn, 'wb') as f:
        pickle.dump(detail_error, f)