# Koh Lanta Emergency Referral Clinical Research Form (Online CRF)
### โครงการวิจัย: ความทันเวลา ปัจจัยกำหนดความล่าช้า และผลลัพธ์ทางคลินิกระยะแรกของการส่งต่อผู้ป่วยฉุกเฉินจากโรงพยาบาลชุมชนบนเกาะสู่โรงพยาบาลรับส่งต่อบนแผ่นดินใหญ่: การศึกษาตามรุ่นย้อนหลัง
*(Timeliness, delay determinants, and early clinical outcomes of emergency transfers from an island district hospital to a mainland referral hospital: a retrospective cohort study)*

---

## 🏥 วัตถุประสงค์
ระบบบันทึกและจัดการข้อมูลการวิจัยทางคลินิกออนไลน์ (Clinical Research Electronic Data Capture / Online CRF) สำหรับการเก็บข้อมูลผู้ป่วยฉุกเฉินวิกฤต 3 กลุ่มโรคเป้าหมายที่ได้รับการส่งต่อจาก **โรงพยาบาลเกาะลันตา** ไปยัง **โรงพยาบาลกระบี่**:
1. **STEMI / Acute Coronary Syndrome (ACS)**
2. **Acute Stroke**
3. **Severe Trauma (บาดเจ็บรุนแรง)**

---

## 📋 โครงสร้างแบบบันทึกข้อมูล (CRF Forms)
- **Form 1: ข้อมูลพื้นฐานและห้องฉุกเฉินเกาะลันตา (Baseline Demographics & Island ED Care)**
  - คัดกรอง Inclusion / Exclusion criteria
  - ข้อมูลประชากรศาสตร์, สัญญาณชีพแรกรับ, โรคประจำตัว (Charlson Comorbidity Index)
  - คะแนนความรุนแรง (Killip, GCS, Revised Trauma Score) และช่วงเวลา DIDO
- **Form 2: เส้นทางเวลาและเหตุการณ์ระหว่างนำส่ง (Micro-Timeline T0–T5 & En-route Adverse Events)**
  - รายละเอียดจุดหมุดเวลา T0 (ถึง ER เกาะลันตา) -> T1 (ออกจากเกาะ) -> T2 (ถึงท่าเรือคลองหมาก) -> T3 (ขึ้น/ลงแพขนานยนต์) -> T4 (ถึง ER รพ.กระบี่) -> T5 (เริ่มหัตถการจำเพาะ)
  - ตรวจจับช่วงเวลาเดินแพขนานยนต์อัตโนมัติตาม T2 (Daytime 06:00–22:00 น. / Off-Hour Standby 22:00–06:00 น.)
  - การเฝ้าระวังสัญญาณชีพระหว่างนำส่ง และเหตุการณ์ไม่พึงประสงค์ (Cardiac arrest, CPR, Intubation, Escalation)
- **Form 3: ข้อมูลสภาพแวดล้อมและอุทก-อุตุนิยมวิทยา (Hydro-Meteorological & Environmental Data)**
  - ระดับน้ำทะเล (Tidal height), ความเสี่ยงสันทราย (Sandbar hazard), คลื่นลมทะเล (Beaufort Sea state)
  - ปริมาณฝน, ฤดูกาลการท่องเที่ยว (Monsoon / High season), วันหยุดราชการ, กะการทำงาน
- **Form 4: การรักษาจำเพาะและผลลัพธ์ทางคลินิก รพ.กระบี่ (Mainland Interventions & Outcomes)**
  - การรักษาตามกลุ่มโรค (PCI, Thrombolysis, Emergency OR, CT Scan)
  - ประเมินกรอบเวลาวิกฤต (Golden Windows: D2B $\le$ 180 min, O2N $\le$ 270 min, Golden Hour)
  - ผลลัพธ์ทางคลินิก (Deterioration, In-hospital mortality, ความยาวนานวันนอน, สถานะจำหน่าย)

---

## 🚀 ฟังก์ชันการใช้งาน
- **บันทึกข้อมูลอัตโนมัติ (Auto-Save):** บันทึกลงใน Local Storage ภายในเบราว์เซอร์อย่างปลอดภัย
- **คำนวณคะแนนและช่วงเวลาทันที (Real-time Calculations):** CCI, RTS, DIDO, Transit durations, Golden windows
- **Admin Dashboard:** จัดการเคส ตรวจสอบรายงานสรุป สถิติภาพรวม แผนภูมิ และค้นหาเคส
- **Export ข้อมูล:** ส่งออกฐานข้อมูล Master และ Form 1-4 เป็นไฟล์ Excel (.xlsx) และ PDF Report

---

## 🌐 เข้าใช้งานระบบออนไลน์
เข้าใช้งานได้โดยตรงผ่าน GitHub Pages:  
👉 **[https://nutt2539.github.io/lanta-referral-crf/](https://nutt2539.github.io/lanta-referral-crf/)**
