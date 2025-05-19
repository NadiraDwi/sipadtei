-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 19, 2025 at 07:02 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sipadtei_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` char(4) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `nama`, `username`, `password`) VALUES
('A001', 'Radin', 'rdnbn_adm', 'c93ccd78b2076528346216b3b2f701e6'),
('A002', 'Sheren', 'shrn', '1eea36fbd4f4919251e3192dce2da380');

-- --------------------------------------------------------

--
-- Stand-in structure for view `detail_mk`
-- (See below for the actual view)
--
CREATE TABLE `detail_mk` (
`kode_mk` char(10)
,`mata_kuliah` varchar(255)
,`kategori` varchar(100)
,`dosen` varchar(100)
,`offering` char(10)
,`hari` varchar(20)
,`jam_awal` int
,`jam_akhir` int
,`kode_ruang` char(10)
,`max_peserta` int
,`jml_peserta` int
,`admin` varchar(100)
);

-- --------------------------------------------------------

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `nidn` char(20) NOT NULL,
  `nama_dosen` varchar(100) DEFAULT NULL,
  `jabatan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dosen`
--

INSERT INTO `dosen` (`nidn`, `nama_dosen`, `jabatan`) VALUES
('0014016308', 'Dr. Wahyu Sakti Gunawan Irianto, M.Kom.\r\n\r\n', 'Lektor Kepala\r\n\r\n'),
('0015201189', 'Moh. Muzayyin Amrulloh, S.Kom., M.Kom.\r\n\r\n', 'Tenaga Dosen'),
('0017028902', 'Gres Dyah Kusuma Ningrum, S.Pd., M.Pd.\r\n\r\n', 'Asisten Ahli\r\n\r\n'),
('111111111', 'aaaaaaaaaaaa', 'aaaaaaaaa');

-- --------------------------------------------------------

--
-- Table structure for table `dosen_mk`
--

CREATE TABLE `dosen_mk` (
  `kode_mk` char(10) DEFAULT NULL,
  `nidn` char(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dosen_mk`
--

INSERT INTO `dosen_mk` (`kode_mk`, `nidn`) VALUES
('PTIN236005', '0017028902'),
('PTIN236008', '0014016308'),
('PTIN236008', '0015201189');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_jadwal` char(5) NOT NULL,
  `hari` varchar(20) DEFAULT NULL,
  `jam_awal` int DEFAULT NULL,
  `jam_akhir` int DEFAULT NULL,
  `kode_ruang` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_jadwal`, `hari`, `jam_awal`, `jam_akhir`, `kode_ruang`) VALUES
('J001', 'Senin ', 1, 3, 'A19-704'),
('J002', 'Rabu', 4, 6, 'B11-201');

-- --------------------------------------------------------

--
-- Table structure for table `kategori`
--

CREATE TABLE `kategori` (
  `id_kategori` char(4) NOT NULL,
  `nama_kategori` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kategori`
--

INSERT INTO `kategori` (`id_kategori`, `nama_kategori`) VALUES
('K001', 'Teori'),
('K002', 'Praktikum');

-- --------------------------------------------------------

--
-- Table structure for table `matakuliah`
--

CREATE TABLE `matakuliah` (
  `kode_mk` char(10) NOT NULL,
  `mata_kuliah` varchar(255) DEFAULT NULL,
  `id_kategori` char(4) DEFAULT NULL,
  `id_off` char(10) DEFAULT NULL,
  `id_jadwal` char(5) DEFAULT NULL,
  `jml_peserta` int DEFAULT NULL,
  `id_admin` char(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `matakuliah`
--

INSERT INTO `matakuliah` (`kode_mk`, `mata_kuliah`, `id_kategori`, `id_off`, `id_jadwal`, `jml_peserta`, `id_admin`) VALUES
('PTIN236000', 'Pemrograman Berorientasi Obyek', 'K002', 'O24PTIC', 'J001', 30, 'A002'),
('PTIN236005', 'Matematika Diskrit', 'K001', 'O24PTIA', 'J001', 36, 'A001'),
('PTIN236008', 'Struktur Data', 'K002', 'O24PTIA', 'J002', 34, 'A002');

--
-- Triggers `matakuliah`
--
DELIMITER $$
CREATE TRIGGER `trg_cek_jml_peserta_matakuliah_insert` BEFORE INSERT ON `matakuliah` FOR EACH ROW BEGIN
    DECLARE max_allowed INT;
    SELECT r.max_peserta INTO max_allowed
    FROM Jadwal j
    JOIN Ruang r ON j.kode_ruang = r.kode_ruang
    WHERE j.id_jadwal = NEW.id_jadwal;
    IF NEW.jml_peserta > max_allowed THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR: Jumlah peserta melebihi kapasitas maksimal ruang!';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `offering`
--

CREATE TABLE `offering` (
  `id_off` char(10) NOT NULL,
  `nama_off` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `offering`
--

INSERT INTO `offering` (`id_off`, `nama_off`) VALUES
('O24PTIA', 'S1 Pendidikan Teknik Informatika A'),
('O24PTIB', 'S1 Pendidikan Teknik Informatika B'),
('O24PTIC', 'S1 Pendidikan Teknik Informatika C');

-- --------------------------------------------------------

--
-- Table structure for table `ruang`
--

CREATE TABLE `ruang` (
  `kode_ruang` char(10) NOT NULL,
  `id_kategori` char(4) DEFAULT NULL,
  `gedung` varchar(50) DEFAULT NULL,
  `lantai` int DEFAULT NULL,
  `ruang` int DEFAULT NULL,
  `max_peserta` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ruang`
--

INSERT INTO `ruang` (`kode_ruang`, `id_kategori`, `gedung`, `lantai`, `ruang`, `max_peserta`) VALUES
('A19-704', 'K001', 'A19', 7, 4, 40),
('B11-201', 'K002', 'B11', 2, 1, 40);

-- --------------------------------------------------------

--
-- Structure for view `detail_mk`
--
DROP TABLE IF EXISTS `detail_mk`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `detail_mk`  AS SELECT `m`.`kode_mk` AS `kode_mk`, `m`.`mata_kuliah` AS `mata_kuliah`, `k`.`nama_kategori` AS `kategori`, `d`.`nama_dosen` AS `dosen`, `m`.`id_off` AS `offering`, `j`.`hari` AS `hari`, `j`.`jam_awal` AS `jam_awal`, `j`.`jam_akhir` AS `jam_akhir`, `r`.`kode_ruang` AS `kode_ruang`, `r`.`max_peserta` AS `max_peserta`, `m`.`jml_peserta` AS `jml_peserta`, `a`.`nama` AS `admin` FROM (((((((`matakuliah` `m` join `kategori` `k` on((`m`.`id_kategori` = `k`.`id_kategori`))) join `offering` `o` on((`o`.`id_off` = `m`.`id_off`))) join `jadwal` `j` on((`j`.`id_jadwal` = `m`.`id_jadwal`))) join `admin` `a` on((`a`.`id_admin` = `m`.`id_admin`))) join `ruang` `r` on((`r`.`kode_ruang` = `j`.`kode_ruang`))) join `dosen_mk` `dmk` on((`dmk`.`kode_mk` = `m`.`kode_mk`))) join `dosen` `d` on((`d`.`nidn` = `dmk`.`nidn`)))  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`nidn`);

--
-- Indexes for table `dosen_mk`
--
ALTER TABLE `dosen_mk`
  ADD KEY `kode_mk` (`kode_mk`,`nidn`),
  ADD KEY `nidn` (`nidn`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `kode_ruang` (`kode_ruang`);

--
-- Indexes for table `kategori`
--
ALTER TABLE `kategori`
  ADD PRIMARY KEY (`id_kategori`);

--
-- Indexes for table `matakuliah`
--
ALTER TABLE `matakuliah`
  ADD PRIMARY KEY (`kode_mk`),
  ADD KEY `id_kategori` (`id_kategori`,`id_off`,`id_jadwal`),
  ADD KEY `id_admin` (`id_admin`),
  ADD KEY `id_off` (`id_off`),
  ADD KEY `id_jadwal` (`id_jadwal`);

--
-- Indexes for table `offering`
--
ALTER TABLE `offering`
  ADD PRIMARY KEY (`id_off`);

--
-- Indexes for table `ruang`
--
ALTER TABLE `ruang`
  ADD PRIMARY KEY (`kode_ruang`),
  ADD KEY `id_kategori` (`id_kategori`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dosen_mk`
--
ALTER TABLE `dosen_mk`
  ADD CONSTRAINT `dosen_mk_ibfk_1` FOREIGN KEY (`kode_mk`) REFERENCES `matakuliah` (`kode_mk`),
  ADD CONSTRAINT `dosen_mk_ibfk_2` FOREIGN KEY (`nidn`) REFERENCES `dosen` (`nidn`);

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`kode_ruang`) REFERENCES `ruang` (`kode_ruang`);

--
-- Constraints for table `matakuliah`
--
ALTER TABLE `matakuliah`
  ADD CONSTRAINT `matakuliah_ibfk_1` FOREIGN KEY (`id_kategori`) REFERENCES `kategori` (`id_kategori`),
  ADD CONSTRAINT `matakuliah_ibfk_2` FOREIGN KEY (`id_off`) REFERENCES `offering` (`id_off`),
  ADD CONSTRAINT `matakuliah_ibfk_3` FOREIGN KEY (`id_jadwal`) REFERENCES `jadwal` (`id_jadwal`),
  ADD CONSTRAINT `matakuliah_ibfk_4` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Constraints for table `ruang`
--
ALTER TABLE `ruang`
  ADD CONSTRAINT `ruang_ibfk_1` FOREIGN KEY (`id_kategori`) REFERENCES `kategori` (`id_kategori`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
