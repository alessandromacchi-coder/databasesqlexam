import pandas as pd

df_raw = pd.read_csv('f1.csv', low_memory=False)

#qui va fatta la pulizia che è ancora da fare
#va creata una nuova variabile del df dopo aver pulito quello raw
#qui bisogna trovare 

df_ready=df_raw.copy()

print(df_ready)

df_drivers=#e dobbiamo fare un df per ogni singola tabella
df_libri_finale.columns = ['titolo', 'prezzo', 'id_autore'] # tipo così

#poi sarebbe da fare un .to_sql con il nome tabella ecc per ogni df




