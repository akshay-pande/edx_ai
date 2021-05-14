import pandas as pd
import math

alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]

def process_data_frame(df, a, wts, n_iter):

    new_wts = wts
    x = []
    n = df.shape[0]    
    
    for j in range(0, n_iter):
        wts = new_wts        
        for i in range(0,len(wts)):
            summ = 0
            cost_fn = 0
            for row in range(0,n):

                x = [1,df.loc[row]['x1'],df.loc[row]['x2']]
                y = df.loc[row]['y']

                f_x = wts[0] + wts[1]*x[1] + wts[2]*x[2] 
                
                summ += (f_x - y)*x[i]
             #  cost_fn += (f_x- y)**2
            
            
            new_wts[i] -= summ*(a/n)
            #cost_fn = cost_fn/(2*n)            

    return new_wts


def normalize_df(df):
    means = []
    stddev = []
    new_df = df.copy()
    for col in df:
        means.append(df[col].mean())
        stddev.append(df[col].std())

    for row in range(0,df.shape[0]):
        new_x1 = (df.loc[row,'x1']-means[0])/stddev[0]
        new_x2 = (df.loc[row,'x2']-means[1])/stddev[1]
        y = df.loc[row,'y']
    
        new_df.loc[row] = [new_x1, new_x2, y]        

    return new_df
    
    
def main():
    out_row = 0
    df_inp = pd.read_csv('input2.csv', header=None)
    df_inp.columns = ['x1','x2','y']   
    normalized_df = normalize_df(df_inp)   
    orig_weights = [0, 0, 0]
    out_df = pd.DataFrame(columns = ['a','iter','b0','b1','b2'])

    for a in alpha:
              
        new_weights = process_data_frame(normalized_df, a, [0,0,0], 100)
        output = [a, 100]
        output.extend(new_weights)        
        out_df.loc[out_row] = output
        out_row = out_row + 1  
        print("alpha= ", a, " ", new_weights)

    
    new_weights = process_data_frame(normalized_df, 0.1, orig_weights, 200)
    print("alpha final ", new_weights)
    output = [0.1, 200]
    output.extend(new_weights)
    out_df.loc[out_row] = output
    out_df.to_csv('output2.csv', header=False, index=False)
   

if __name__ == "__main__":
    main()
