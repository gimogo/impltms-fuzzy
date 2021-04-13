import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


print('=====Seleksi Magang======')
aa = input('masukan list data mhsw (.csv) = ')

#read data csv
def read_data():
    reader = pd.read_csv(aa,delimiter=',')
    return np.array(reader)

def read_data_prediction():
    reader = pd.read_csv('Prediksi.csv',delimiter=',')
    return np.array(reader)

#Save to file
def save_to_file(array_data):
    np.savetxt\
        ('Prediksi.csv', array_data, fmt='%s', delimiter=',',
         header="NRP, Tes Kompetensi, Kepribadian, Diterima")

#kompetensi
def kompetensi_rendah(x):
    if x <= 35: return  1
    elif 35 < x < 60 : return float((60-x)/(60-35))
    else: return 0
def kompetensi_sedang(x):
    if 45 < x <= 65 : return float((x-45)/(65-45))
    elif 65 < x < 85 : return float((85-x)/(85-65))
    else : return 0
def kompetensi_tinggi(x):
    if x <= 65 : return 0
    elif 65 < x < 85 : return float((x-65)/(85-65))
    else : return 1

#Kepribadian
def kepribadian_rendah(x):
    if x <= 35: return 1
    elif 35 < x < 60: return float((60 - x) / (60 - 35))
    else: return 0
def kepribadian_sedang(x):
    if 45 < x <= 50: return float((x - 45) / (50 - 45))
    elif 50 < x < 85: return float((85 - x) / (85 - 50))
    else: return 0
def kepribadian_tinggi(x) :
    if x <= 65:return 0
    elif 65 < x < 85: return float((x - 65) / (85 - 65))
    else: return 1

def fuzzification_kompetensi(data):
    data_kompetensi = data[:, 1]
    fuzzy_kompetensi = []
    print('===== Fuzzy Score for Kompetensi =====')
    for x in range(len(data)):
        komp_rendah = kompetensi_rendah(data_kompetensi[x])
        komp_sedang = kompetensi_sedang(data_kompetensi[x])
        komp_tinggi = kompetensi_tinggi(data_kompetensi[x])
        metriks_kompetensi = [komp_rendah, komp_sedang, komp_tinggi]
        fuzzy_kompetensi.append(metriks_kompetensi)
        print('NRP','1520170',x+1, metriks_kompetensi)
    return fuzzy_kompetensi

def fuzzification_kepribadian(data):
    data_kepribadian = data[:, 2]
    fuzzy_kepribadian = []
    print('\n========== Fuzzy Score for Kepribadian ==========')
    for x in range (len(data)):
        kep_rendah = kepribadian_rendah(data_kepribadian[x])
        kep_sedang = kepribadian_sedang(data_kepribadian[x])
        kep_tinggi = kepribadian_tinggi(data_kepribadian[x])
        metriks_kepribadian = [kep_rendah,kep_sedang,kep_tinggi]
        fuzzy_kepribadian.append(metriks_kepribadian)
        print('NRP','1520170',x+1, metriks_kepribadian)
    return fuzzy_kepribadian

#Inferensi
def inference(kompetensi,kepribadian):
    accepted = []
    rejected = []
    kelayakan = []
    print('\n==========  Inference Metrics  ==========')
    for x in range (len(kompetensi)):
        del accepted[:]
        del rejected[:]
        rejected.append(np.minimum(kompetensi[x][0],kepribadian[x][0]))
        rejected.append(np.minimum(kompetensi[x][0],kepribadian[x][1]))
        accepted.append(np.minimum(kompetensi[x][0],kepribadian[x][2]))
        rejected.append(np.minimum(kompetensi[x][1],kepribadian[x][0]))
        rejected.append(np.minimum(kompetensi[x][1],kepribadian[x][1]))
        accepted.append(np.minimum(kompetensi[x][1],kepribadian[x][2]))
        rejected.append(np.minimum(kompetensi[x][2],kepribadian[x][0]))
        accepted.append(np.minimum(kompetensi[x][2],kepribadian[x][1]))
        accepted.append(np.minimum(kompetensi[x][2],kepribadian[x][2]))

        kelayakan_accepted = np.max(accepted)
        kelayakan_rejected = np.max(rejected)
        metriks_kelayakan = [kelayakan_rejected,kelayakan_accepted]
        kelayakan.append(metriks_kelayakan)
        print('NRP','1520170',x + 1, metriks_kelayakan)

    return kelayakan

def mamdani(kelayakan):
    for x in range(1,100, 1):
        if x < 66 :
            low = [np.sum(x*kelayakan[0]), np.sum(kelayakan[0])]
        else:
            high = [np.sum(x * kelayakan[1]), np.sum(kelayakan[1])]
    return (low[0]+high[0])/(low[1]+high[1])

def calculate_accuracy(data, prediction):
    correct = 0
    for x in range(20):
        if data[x][-1] == prediction[x][-1]:
            correct += 1
    print('Akurasi :')
    return (correct / 20) * 100.0

# Plot fungsi keanggotaan Tes Kompetensi
def plot_competency_graph():
    nilai = np.arange(0,100, 1)
    plt.title('Fungsi Keanggotaan Kompetensi')
    plt.plot(nilai, [kompetensi_rendah(x) for x in nilai] , color='red', label='rendah')
    plt.plot(nilai, [kompetensi_sedang(x) for x in nilai] , color='yellow', label='sedang')
    plt.plot(nilai, [kompetensi_tinggi(x) for x in nilai] , color='blue', label='tinggi')
    plt.legend()
    plt.savefig('fungsi_keanggotaan_kompetensi.png')
    plt.show()

def plot_personality_graph():
    nilai = np.arange(0,100, 1)
    plt.title('Fungsi Keanggotaan Kepribadian')
    plt.plot(nilai, [kepribadian_rendah(x) for x in nilai] , color='red', label='rendah')
    plt.plot(nilai, [kepribadian_sedang(x) for x in nilai] , color='yellow', label='sedang')
    plt.plot(nilai, [kepribadian_tinggi(x) for x in nilai] , color='blue', label='tinggi')
    plt.legend()
    plt.savefig('fungsi_keanggotaan_kepribadian.png')
    plt.show()


def main():
    rate = []
    data = read_data()
    fuzzy_kompetensi = fuzzification_kompetensi(data)
    fuzzy_kepribadian = fuzzification_kepribadian(data)
    kelayakan = inference(fuzzy_kompetensi,fuzzy_kepribadian)

    print('\n==============================================')
    for x in range(len(kelayakan)):
        crisp = mamdani(kelayakan[x])
        print('NRP','1520170',x+1,'=',crisp)
        
        if crisp <= 65 :
            data[x][-1] = "Tidak"
        else :
            data[x][-1] = "Ya"
    save_to_file(data)

    #Calculate Accuracy
    print('\n>>Menghitung Akurasi<<')
    data_real = read_data()
    data_prediction  = read_data_prediction()
    rate = calculate_accuracy(data_real,data_prediction)
    print(rate,'%','diterima.. semangat!!')

    #Show graph plot
    plot_competency_graph()
    plot_personality_graph()

main()

