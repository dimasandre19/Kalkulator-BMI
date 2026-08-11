def pilih_opsi(prompt, opsi):
    opsi_lower = [o.lower() for o in opsi]
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban in opsi_lower:
            return jawaban
        print(f"Masukkan salah satu dari: {', '.join(opsi)}")


def isi_matriks_segitiga(N, orientasi, nama):
    M = [["" for _ in range(N)] for _ in range(N)]
    print(f"\nMasukkan nilai untuk {nama} ({N}x{N} - Segitiga {orientasi.capitalize()}):")
    for i in range(N):
        for j in range(N):
            if (orientasi == 'atas' and i <= j) or (orientasi == 'bawah' and i >= j):
                M[i][j] = input(f"{nama}[{i+1}][{j+1}] = ")
    return M


def isi_bawah(Nm1, nama):
    M = [["" for _ in range(Nm1)] for _ in range(Nm1)]
    print(f"\nMasukkan nilai untuk {nama} ({Nm1}x{Nm1} - Segitiga Bawah):")
    for i in range(Nm1):
        for j in range(Nm1):
            if i >= j:
                M[i][j] = input(f"{nama}[{i+1}][{j+1}] = ")
    return M


def cetak_matriks(judul, M):
    print(f"\n{judul}:")
    for baris in M:
        print(" ".join(f"{str(x):>3}" if str(x) != '' else f"{'0':>3}" for x in baris))


def transpose(M):
    N = len(M)
    T = [["" for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            T[j][i] = M[i][j]
    return T


def gabung_tipe1(A, B):
    N = len(A)
    C = [["" for _ in range(N)] for _ in range(N)]
    # Letakkan A
    for i in range(N):
        for j in range(N):
            if A[i][j] != "":
                C[i][j] = A[i][j]
    # Letakkan B digeser 1 baris
    Nm1 = len(B)
    for i in range(Nm1):
        for j in range(Nm1):
            if i >= j and B[i][j] != "":
                C[i+1][j] = B[i][j]
    return C


def gabung_tipe3(A, B):
    N = len(A)
    B_transpose = transpose(B)
    C = [["" for _ in range(N)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            if i <= j:
                C[i][j] = A[i][j] if A[i][j] != "" else "0"
            else:
                C[i][j] = B_transpose[i][j] if B_transpose[i][j] != "" else "0"
    return C


def main():
    print("=== PROGRAM ARRAY SEGITIGA TIPE 1 DAN 3 ===")
    print("Hanya boleh ukuran matriks antara 3 sampai 5\n")

    while True:
        try:
            N = int(input("Masukkan ukuran matriks N (3–5): "))
            if 3 <= N <= 5:
                break
            else:
                print("Ukuran N harus antara 3 dan 5.")
        except ValueError:
            print("Masukkan angka antara 3 dan 5.")

    tipe = pilih_opsi("Pilih tipe (1 atau 3): ", ["1", "3"]) 

    if tipe == "1":
        A = isi_matriks_segitiga(N, 'atas', "A")
        
        if N <= 1:
            B = []
        else:
            B = isi_bawah(N-1, "B")
        
        C = gabung_tipe1(A, B if B else [[""]])

        print("\n" + "=" * 50)
        print("HASIL ARRAY GABUNGAN - TIPE 1")
        print("=" * 50)
        
        cetak_matriks(f"Array A ({N}x{N} - Segitiga Atas)", A)
        if N > 1:
            cetak_matriks(f"Array B ({N-1}x{N-1} - Segitiga Bawah)", B)
        cetak_matriks(f"Array C ({N}x{N} - Gabungan A dan B)", C)
        
    else:
        print("\n=== TIPE 3: Transpose Array B ===")
        A = isi_matriks_segitiga(N, 'atas', "A")
        B = isi_matriks_segitiga(N, 'atas', "B")
        C = gabung_tipe3(A, B)

        print("\n" + "=" * 50)
        print("HASIL ARRAY GABUNGAN - TIPE 3")
        print("=" * 50)
        
        cetak_matriks(f"Array A ({N}x{N} - Segitiga Atas)", A)
        cetak_matriks(f"Array B ({N}x{N} - Segitiga Atas)", B)
        
        B_T = transpose(B)
        cetak_matriks(f"Array B Transpose ({N}x{N})", B_T)
        cetak_matriks(f"Array C ({N}x{N} - Gabungan A dan B')", C)


if __name__ == "__main__":
    main()