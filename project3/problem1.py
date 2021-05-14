import pandas as pd
import math

#Linear Regression

w1 = 0
w2 = 0
w0 = 0

def process_data_frame(df, w0, w1, w2):
    
    for row in range(0,df.shape[0]):
        
        x1 = df.loc[row][0]
        x2 = df.loc[row][1]
        y = df.loc[row][2]

        f_x = math.copysign(1,w0 + w1*x1 + w2*x2)
        
        if ( f_x != y):
             w0 = w0 + 1*y
             w1 = w1 + x1*y
             w2 = w2 + x2*y             

    return (w0,w1,w2)
    
def main():
    out_row = 0
    df_inp = pd.read_csv('input1.csv', header=None)
    orig_weights = (w0, w1, w2)     
    new_weights = process_data_frame(df_inp, w0, w1, w2)
    out_df = pd.DataFrame([[new_weights[1], new_weights[2], new_weights[0]]])    

    while orig_weights != new_weights:
        out_row = out_row + 1
        orig_weights = new_weights
        new_weights = process_data_frame(df_inp, orig_weights[0],
                                         orig_weights[1], orig_weights[2])
        out_df.loc[out_row] = [ new_weights[1], new_weights[2],new_weights[0]]       

    out_df.to_csv('output1.csv', header=False, index=False)
   

if __name__ == "__main__":
    main()
