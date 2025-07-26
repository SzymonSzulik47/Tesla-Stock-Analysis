import yfinance as yf
import pandas as pd

#Parametry pobierania danych
symbol = "TSLA"
start_date = "2021-07-01"
end_date = "2024-07-25"

#Pobieranie i zapis danych
tesla_data = yf.download(symbol, start=start_date, end=end_date)[['Open', 'High', 'Low', 'Close', 'Volume']]

#Reset indeksu i zapis jako CSV bez dodatkowych nagłówków
tesla_data.reset_index().to_csv("tesla_stock_data.csv", index=False)

#Wczytanie danych CSV z poprawnym typem daty
tesla_data = pd.read_csv("tesla_stock_data.csv", parse_dates=["Date"])
tesla_data.set_index("Date", inplace=True)

#Debug: pokaż zakres dat
print("Zakres dat:", tesla_data.index.min(), "do", tesla_data.index.max())

#Daty raportów
earnings_dates = [
    "2021-07-26", "2021-10-20", "2022-01-26", "2022-04-20", "2022-07-20",
    "2022-10-19", "2023-01-25", "2023-04-19", "2023-07-19", "2023-10-18",
    "2024-01-24", "2024-04-23", "2024-07-23"
]
earnings_dates = pd.to_datetime(earnings_dates)

#Analiza reakcji cen
results = []

for date in earnings_dates:
    try:
        price_before = float(tesla_data.loc[:date].iloc[-1]['Close'])
        price_next_day = float(tesla_data.loc[date + pd.Timedelta(days=1):].iloc[0]['Close'])
        price_next_week = float(tesla_data.loc[date + pd.Timedelta(days=7):].iloc[0]['Close'])

        results.append({
            "Report Date": date.date(),
            "Price Before": price_before,
            "Price +1 Day": price_next_day,
            "Price +7 Days": price_next_week,
            "Change 1D (%)": round((price_next_day - price_before) / price_before * 100, 2),
            "Change 7D (%)": round((price_next_week - price_before) / price_before * 100, 2)
        })
    except Exception as e:
        print(f"Problem z datą {date.date()}: {e}")
        print(f"Czy {date.date()} jest w indeksie danych? {'Tak' if date in tesla_data.index else 'Nie'}")
df_results = pd.DataFrame(results)
print("\nWyniki analizy:")
print(df_results)

#Wykres liniowy
import matplotlib.pyplot as plt
import pandas as pd

results_df = pd.DataFrame(results)

plt.figure(figsize=(10,6))
plt.plot(results_df["Report Date"], results_df["Change 1D (%)"], marker='o', label='Zmiana 1D (%)')
plt.plot(results_df["Report Date"], results_df["Change 7D (%)"], marker='o', label='Zmiana 7D (%)')
plt.xticks(rotation=45)
plt.xlabel("Data raportu")
plt.ylabel("Zmiana ceny (%)")
plt.title("Reakcja ceny akcji Tesli na raporty kwartalne")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Wykres słupkowy zmian procentowych (1D i 7D obok siebie)
plt.figure(figsize=(12, 7))
bar_width = 0.35
index = range(len(results_df["Report Date"]))

plt.bar([i - bar_width/2 for i in index], results_df["Change 1D (%)"], bar_width, label='Zmiana 1D (%)', color='skyblue')
plt.bar([i + bar_width/2 for i in index], results_df["Change 7D (%)"], bar_width, label='Zmiana 7D (%)', color='lightcoral')

plt.xlabel("Data raportu")
plt.ylabel("Zmiana ceny (%)")
plt.title("Reakcja ceny akcji Tesli na raporty kwartalne (porównanie 1D i 7D)")
plt.xticks(index, [d.strftime('%Y-%m') for d in results_df["Report Date"]], rotation=45)
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()
#Wykres rozrzutu (Scatter plot) zmiany 1D vs 7D

plt.figure(figsize=(8, 6))
plt.scatter(results_df["Change 1D (%)"], results_df["Change 7D (%)"], color='purple', alpha=0.7)
plt.xlabel("Zmiana 1D (%)")
plt.ylabel("Zmiana 7D (%)")
plt.title("Korelacja między zmianą 1D a 7D po raportach Tesli")
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8)
plt.axvline(0, color='grey', linestyle='--', linewidth=0.8)
plt.grid(True)
plt.tight_layout()
plt.show()

#Histogram zmian procentowych (1D i 7D)
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(results_df["Change 1D (%)"], bins=10, color='lightgreen', edgecolor='black')
plt.xlabel("Zmiana 1D (%)")
plt.ylabel("Częstość")
plt.title("Rozkład zmian 1D po raportach Tesli")
plt.grid(axis='y', alpha=0.75)

plt.subplot(1, 2, 2)
plt.hist(results_df["Change 7D (%)"], bins=10, color='lightsalmon', edgecolor='black')
plt.xlabel("Zmiana 7D (%)")
plt.ylabel("Częstość")
plt.title("Rozkład zmian 7D po raportach Tesli")
plt.grid(axis='y', alpha=0.75)

plt.tight_layout()
plt.show()
