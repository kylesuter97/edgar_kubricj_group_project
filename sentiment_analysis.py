import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from scipy.stats import pearsonr
import numpy as np

def analysis(sentiment_df, financials_df):
    #temp_data = pd.read_csv('fulloutput.csv')
    temp_data = sentiment_df
    sentiment_df = pd.DataFrame(temp_data)
    sentiment_df['FilingDate'] = pd.to_datetime(sentiment_df['FilingDate'])


    #stock_data = pd.read_csv('stock_returns_daily_2000_now.csv')
    stock_data = financials_df
    ref_data_df = pd.DataFrame(stock_data)
    ref_data_df.isnull().sum()
    sentiment_df.isnull().sum()
    ref_data_df = ref_data_df.replace(np.nan, 0)
    sentiment_df = sentiment_df.replace(np.nan, 0)

    TEST_DF = pd.merge(ref_data_df, sentiment_df, how='inner', left_on=['symbol','date']
                    , right_on=['Symbol','FilingDate'])

    df_train, df_test = train_test_split(TEST_DF, test_size=0.2, random_state=11)

    return_days = [1,2,3,5,10]

    for i in return_days:
        print('*------------------------------------------------------------------*')
        features = ['Positive','Negative','Uncertainty','Litigious','Constraining','Modal']

        # Construct X_train and X_test, y_train and y_test
        X_train = df_train[features]
        y_train = df_train[f'{i}daily_return']

        X_test = df_test[features]
        y_test = df_test[f'{i}daily_return']

        model = LinearRegression()
        model.fit(X_train, y_train)

        # Displays coefficients in df format.
        coef_list = model.coef_.tolist()
        coef_df = pd.DataFrame({'Features': features, 'Coefficients':coef_list})
        print(coef_df)

        #Do predictions:
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test,y_pred)

        print(f"R-squared for feature {i}daily_return is {r2}")
        print(f'MSE (test)  : {mse:.4f}')
        print(f'RMSE (test) : {mse**0.5:.4f}')
        print(f'MAE (test)  : {mae:.4f}')

        for feature in features:
            sns.lmplot(x=feature, y=f'{i}daily_return', data=TEST_DF, palette='Set1')
            #plt.savefig(rf'C:\\Users\\JonUphoff\\Downloads\\NewEdgar\\graphs\\{i}daily_return-by-{feature}-sentiment.png', bbox_inches='tight')
            plt.savefig(rf'{i}daily_return-by-{feature}-sentiment.png', bbox_inches='tight')
            plt.pause(0.001)
            plt.close()


        plt.show(block=False)
        plt.pause(0.001)