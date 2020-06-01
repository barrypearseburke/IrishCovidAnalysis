import matplotlib.pyplot as plt
import pandas

from get_all_data import get_all_dfs

all_data= get_all_dfs()


# Show Data
plt.plot(all_data['df_2017'].Week_number, all_data['df_2017'].Value, label="17", color='#038796')
plt.plot(all_data['df_2018'].Week_number, all_data['df_2018'].Value, label="18", color='#035496')
plt.plot(all_data['df_2019'].Week_number, all_data['df_2019'].Value, label="19", color='#032096')
plt.plot(all_data['df_average'].Week_number, all_data['df_average'].average, label="17-19_ave", color='#54ff0a')
plt.plot(all_data['df_2020'].Week_number, all_data['df_2020'].Value, label="20", color='#e1fa41')
plt.plot(all_data['df2020_without_covid'].Week_number, all_data['df2020_without_covid'].Value, label="20_exc_covid", color='#db3b41')

plt.grid()
plt.xticks(pandas.np.arange(min(all_data['df_2017'].Week_number), max(all_data['df_2017'].Week_number) + 1, 1.0))
plt.legend()
plt.xlabel("Week_number")
plt.ylabel("Deaths")
plt.show()


