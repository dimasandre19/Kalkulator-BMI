# PROJECT PERHITUNGAN BMI

print("Perhitungan BMI (Body Mass Index)")
print("---------------------------------")

berat_badan = input("Masukkan berat badan anda (kilogram): ")
berat_badan = float(berat_badan)
tinggi_badan = input("Masukkan tinggi badan anda (meter): ")
tinggi_badan = float(tinggi_badan)

if tinggi_badan <= 0:
    print("Error: Tinggi badan harus lebih dari 0!")
else:
    bmi = berat_badan / (tinggi_badan ** 2)

berat_badan_ideal = dict()
berat_badan_ideal['bawah'] = 18.5*(tinggi_badan**2)
berat_badan_ideal['atas'] = 25*(tinggi_badan**2)

print(f"Nilai BMI anda adalah {bmi:.2f} kg/m^2")
print("Nilai BMI normal adalah 18.5 kg/m^2 - 25 kg/m^2")
print(f"Berat badan ideal anda adalah dalam rentang "
      f"{berat_badan_ideal['bawah']:.2f} - {berat_badan_ideal['atas']:.2f}")

# Menentukan kategori BMI
if bmi < 18.5:
        kategori = "Kurus (Underweight)"
elif 18.5 <= bmi < 25:
        kategori = "Normal"
elif 25 <= bmi < 30:
        kategori = "Gemuk (Overweight)"
else:
        kategori = "Obesitas"

print(f"Kategori BMI anda: {kategori}")


print("--------------------------------------------")
print("Terima kasih sudah menggunakan program ini:)")