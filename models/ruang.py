class Kategori:
    def __init__(self, id_kategori, nama_kategori):
        self.id_kategori = id_kategori
        self.nama_kategori = nama_kategori


class Ruang(Kategori):
    def __init__(self, kode_ruang, gedung, lantai, ruang, max_peserta, id_kategori, nama_kategori):
        super().__init__(id_kategori, nama_kategori)
        self.kode_ruang = kode_ruang
        self.gedung = gedung
        self.lantai = lantai
        self.ruang = ruang
        self.max_peserta = max_peserta