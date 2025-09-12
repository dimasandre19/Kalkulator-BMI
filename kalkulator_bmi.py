# PROJECT PERHITUNGAN BMI

print("Perhitungan BMI (Body Mass Index)")
print("---------------------------------")

berat_badan = float(input("Masukkan berat badan anda (kilogram): "))
tinggi_badan = float(input("Masukkan tinggi badan anda (meter): "))

if tinggi_badan <= 0:
    print("Error: Tinggi badan harus lebih dari 0!")
else:
    bmi = berat_badan / (tinggi_badan ** 2)

berat_badan_ideal = dict()
berat_badan_ideal['bawah'] = 18.5*(tinggi_badan**2)
berat_badan_ideal['atas'] = 25*(tinggi_badan**2)

if bmi < 18.5:
        kategori = "Kurus (Underweight)"
elif 18.5 <= bmi < 25:
        kategori = "Normal" 
elif 25 <= bmi < 30:
        kategori = "Gemuk (Overweight)"
else:
        kategori = "Obesitas"

print(f"\nHasil Kalkulator BMI adalah:")
print("............................")
print(f"Nilai BMI anda adalah {bmi:.2f} kg/m^2")
print(f"Kategori anda adalah: {kategori}")
print(f"Berat badan ideal anda adalah dalam rentang "
      f"{berat_badan_ideal['bawah']:.2f} - {berat_badan_ideal['atas']:.2f}")

print("--------------------------------------------")
print("Terima kasih sudah menggunakan program ini:)")