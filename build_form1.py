# -*- coding: utf-8 -*-
"""
Form 1 HTML Generator module
"""

def get_form1_html():
    return """
    <div id="page-form1" class="crf-page theme-form1 active">
        <!-- Header Box -->
        <div class="doc-header-box">
            <h2>แบบบันทึกข้อมูลการวิจัยทางคลินิก (CASE RECORD FORM: CRF)</h2>
            <h3>ส่วนที่ 1: การคัดกรอง ข้อมูลประชากรศาสตร์ และคะแนนความรุนแรงทางคลินิก ณ รพ.เกาะลันตา</h3>
            <p>Form 1: Patient Eligibility, Demographics & Island ED Baseline Evaluation</p>
        </div>

        <!-- Table 1: Identifiers -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">รหัสวิจัยผู้ป่วย (STUDY_ID)</td>
                <td style="width: 25%;">
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span>LANTA_</span>
                        <input type="text" id="f1_study_id" class="study-id-sync" placeholder="เช่น 001" style="font-weight: 700; color: #1e3a8a;">
                    </div>
                </td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เลขที่ใบส่งต่อ (Refer_ID)</td>
                <td style="width: 25%;">
                    <input type="text" id="f1_refer_id" class="refer-id-sync" placeholder="ระบุเลขที่ใบส่งต่อ">
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">เลขประจำตัวผู้ป่วย (HN / VN เกาะลันตา)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>HN:</span><input type="text" id="f1_hn" class="hn-sync" style="width: 80px;">
                        <span>VN:</span><input type="text" id="f1_vn" class="vn-sync" style="width: 80px;">
                    </div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">วันที่สกัดข้อมูล / ผู้สกัด (Abstractor)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f1_abs_date" class="date-sync" style="width: 125px;">
                        <span>ผู้สกัด:</span><input type="text" id="f1_abstractor" class="abs-sync" style="width: 100px;">
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 1 -->
        <div class="section-header">หมวดที่ 1: การคัดกรองความเข้าเกณฑ์ของการศึกษา</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 8%; text-align: center;">ลำดับ</th>
                    <th style="width: 67%;">เกณฑ์การคัดเข้า (Inclusion Criteria - ต้องมีครบทุกข้อ)</th>
                    <th style="width: 25%; text-align: center;">ผลการตรวจสอบ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="td-center">1</td>
                    <td>ระยะเวลาส่งต่อ: 1 มกราคม 2564 – 31 ธันวาคม 2569</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_inc1" value="yes" onchange="calcScreening()"> ใช่</label>
                            <label class="form-check"><input type="radio" name="f1_inc1" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center">2</td>
                    <td>ผู้ป่วยผู้ใหญ่ อายุตั้งแต่ 18 ปีบริบูรณ์ขึ้นไป</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_inc2" value="yes" onchange="calcScreening()"> ใช่</label>
                            <label class="form-check"><input type="radio" name="f1_inc2" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center">3</td>
                    <td>มีเอกสารการส่งต่อผู้ป่วยฉุกเฉินระหว่างสถานพยาบาล จาก รพ.เกาะลันตา สู่ รพ.กระบี่ ผ่านทางรถพยาบาลและแพขนานยนต์</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_inc3" value="yes" onchange="calcScreening()"> ใช่</label>
                            <label class="form-check"><input type="radio" name="f1_inc3" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700;">4</td>
                    <td id="f1_inc4_cell" style="transition: all 0.3s ease;">
                        <div style="font-weight: 600; color: #1e293b;">ผู้ป่วยฉุกเฉินระดับ ESI 1–2 ใน 3 กลุ่มโรคที่ไวต่อเวลา (3 Time-Sensitive Conditions): <span style="font-size: 12px; color: #dc2626; font-weight: 700;">* บังคับเลือก 1 กลุ่มโรค</span> <span style="font-size: 11px; color: #64748b; font-weight: normal;">(คลิกซ้ำเพื่อเลิกติ๊ก)</span></div>
                        <div style="margin-left: 20px; margin-top: 6px;" class="check-group">
                            <label class="form-check" style="cursor: pointer; padding: 3px 6px; border-radius: 4px;"><input type="radio" name="f1_target_disease" id="f1_inc4_stemi" value="stemi" onchange="syncDiseaseGroup()"> 1. STEMI / Acute Coronary Syndrome (ACS)</label>
                            <label class="form-check" style="cursor: pointer; padding: 3px 6px; border-radius: 4px;"><input type="radio" name="f1_target_disease" id="f1_inc4_ais" value="ais" onchange="syncDiseaseGroup()"> 2. Acute Stroke</label>
                            <label class="form-check" style="cursor: pointer; padding: 3px 6px; border-radius: 4px;"><input type="radio" name="f1_target_disease" id="f1_inc4_trauma" value="trauma" onchange="syncDiseaseGroup()"> 3. Severe Trauma (อุบัติเหตุบาดเจ็บรุนแรง)</label>
                        </div>
                        <div id="f1_inc4_disease_alert" style="margin-top: 8px; padding: 6px 12px; background: #fff1f2; border: 1.5px solid #f43f5e; border-radius: 6px; color: #be123c; font-size: 12.5px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 16px;">⚠️</span>
                            <span><strong>บังคับติ๊กเลือกโรค:</strong> กรุณาเลือก 1 ใน 3 กลุ่มโรคเป้าหมาย (STEMI, Acute Stroke หรือ Severe Trauma)</span>
                        </div>
                        <div id="f1_inc4_disease_selected_badge" style="display: none; margin-top: 6px; padding: 5px 12px; background: #ecfdf5; border: 1.5px solid #10b981; border-radius: 6px; color: #047857; font-size: 12.5px; font-weight: 600;">
                            ✓ <strong>เลือกกลุ่มโรคแล้ว:</strong> <span id="f1_active_disease_name" style="font-weight: 700; color: #065f46;"></span>
                        </div>
                    </td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_inc4" id="f1_inc4_yes" value="yes" onchange="onInc4Change()"> ใช่</label>
                            <label class="form-check"><input type="radio" name="f1_inc4" id="f1_inc4_no" value="no" onchange="onInc4Change()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 8%; text-align: center;">ลำดับ</th>
                    <th style="width: 67%;">เกณฑ์การคัดออก (Exclusion Criteria)</th>
                    <th style="width: 25%; text-align: center;">ผลการตรวจสอบ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="td-center">1</td>
                    <td>เสียชีวิตก่อนนำส่งหรือเสียชีวิตก่อนเคลื่อนย้ายออกจาก รพ.เกาะลันตา (Dead on arrival / Deceased before transfer)</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_exc1" value="yes" onchange="calcScreening()"> ใช่ (คัดออก)</label>
                            <label class="form-check"><input type="radio" name="f1_exc1" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center">2</td>
                    <td>ส่งต่อด้วยอากาศยานทางการแพทย์ (Aeromedical: Sky doctor / HEMS)</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_exc2" value="yes" onchange="calcScreening()"> ใช่ (คัดออก)</label>
                            <label class="form-check"><input type="radio" name="f1_exc2" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center">3</td>
                    <td>ปฏิเสธการส่งต่อ / ขอย้ายไปเอง (Refused transfer / self-transport / DAMA)</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_exc3" value="yes" onchange="calcScreening()"> ใช่ (คัดออก)</label>
                            <label class="form-check"><input type="radio" name="f1_exc3" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="td-center">4</td>
                    <td>ข้อมูลระบุเวลาของผลลัพธ์ไม่ครบถ้วน (Missing essential primary outcome timestamps)</td>
                    <td>
                        <div class="check-row" style="justify-content: center;">
                            <label class="form-check"><input type="radio" name="f1_exc4" value="yes" onchange="calcScreening()"> ใช่ (คัดออก)</label>
                            <label class="form-check"><input type="radio" name="f1_exc4" value="no" onchange="calcScreening()"> ไม่ใช่</label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- สรุปผลการคัดกรอง (Compact 2-Line Automated Screening Banner) -->
        <div id="screening_summary_card" style="padding: 9px 16px; border-radius: 8px; margin-bottom: 18px; transition: all 0.25s ease; border: 2px solid #cbd5e1; background: #f8fafc; display: flex; flex-direction: column; gap: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
            <!-- บรรทัดที่ 1: หัวข้อ + ป้ายสรุปผล + สถานะการล็อก -->
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span id="screening_icon_badge" style="font-size: 17px; line-height: 1;">⚖️</span>
                    <span style="font-weight: 700; font-size: 14.5px; color: #1e293b;">สรุปผลการคัดกรอง:</span>
                    <span id="screening_status_pill" style="font-size: 12.5px; font-weight: 800; padding: 2px 10px; border-radius: 999px; background: #e2e8f0; color: #475569; display: inline-flex; align-items: center; gap: 4px;">
                        ⏳ รอการประเมินเกณฑ์
                    </span>
                </div>
                <div id="screening_lock_indicator" style="font-size: 12px; font-weight: 700;">
                    <!-- Populated dynamically: 🔓 ปลดล็อกระบบ หรือ 🔒 ปิดกั้นการกรอกข้อมูล -->
                </div>
            </div>

            <!-- บรรทัดที่ 2: รายละเอียดสรุปผล / เหตุผลคัดออก -->
            <div id="screening_status_desc" style="font-size: 12px; color: #64748b; line-height: 1.4;">
                กรุณาตอบเกณฑ์การคัดเข้า (Inclusion 4 ข้อ) และเกณฑ์การคัดออก (Exclusion 4 ข้อ) ด้านบนให้ครบถ้วนเพื่อประเมินอัตโนมัติ
            </div>

            <!-- Hidden radio inputs for data persistence / form save without manual clicking -->
            <input type="radio" name="f1_eligible" id="f1_eligible_yes" value="eligible" style="display: none;">
            <input type="radio" name="f1_eligible" id="f1_eligible_no" value="excluded" style="display: none;">
            <span id="screening_badge" class="badge-calc" style="display: none;">Auto-evaluated</span>
        </div>

        <!-- Container for post-screening sections (Locked/Disabled when Excluded) -->
        <div id="f1_post_screening_container" style="transition: all 0.3s ease;">
            <!-- Alert Banner inside Form 1 when Locked -->
            <div id="f1_excluded_lock_alert" style="display: none; background: #fff1f2; border: 2px dashed #e11d48; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 4px;">⛔</div>
                <div style="font-size: 16px; font-weight: 800; color: #9f1239; margin-bottom: 4px;">
                    ปิดกั้นการกรอกข้อมูลในส่วนอื่นๆ ทั้งหมด (Data Entry Locked)
                </div>
                <div style="font-size: 13px; color: #881337; line-height: 1.5;">
                    เคสนี้ไม่ผ่านเกณฑ์การคัดกรองเข้าสู่การศึกษา (Excluded Cohort)<br>
                    ระบบจึงปิดกั้นการบันทึกข้อมูลในหมวด 2–5 (ข้อมูลประชากร, สัญญาณชีพ, DIDO) และแบบบันทึก Form 2, 3, 4 ทั้งหมด<br>
                    <span style="font-size: 12px; color: #64748b;">(หากต้องการแก้ไขความเข้าเกณฑ์ สามารถปรับเปลี่ยนคำตอบในเกณฑ์การคัดเข้า/คัดออกในหมวดที่ 1 ด้านบนได้ทันที)</span>
                </div>
            </div>

        <!-- หมวดที่ 2 -->
        <div class="section-header">หมวดที่ 2: ข้อมูลประชากรศาสตร์และบริบทแรกรับ ณ รพ.เกาะลันตา</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 20%;">ตัวแปร (Variable)</th>
                    <th style="width: 30%;">ข้อมูลที่บันทึก</th>
                    <th style="width: 20%;">ตัวแปร (Variable)</th>
                    <th style="width: 30%;">ข้อมูลที่บันทึก</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">อายุ (Age)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <input type="number" id="f1_age" min="0" max="120" style="width: 90px;" oninput="calcCCI()">
                            <span>ปี (Years)</span>
                            <span id="f1_age_score_badge" class="badge-calc" title="คะแนนอายุ aCCI">+0 คะแนน</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">เพศกำเนิด (Sex)</td>
                    <td>
                        <div class="check-row">
                            <label class="form-check"><input type="radio" name="f1_sex" value="male"> ชาย (Male)</label>
                            <label class="form-check"><input type="radio" name="f1_sex" value="female"> หญิง (Female)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">สถานะประชากร<br>(Residency Status)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f1_residency" value="1"> 1 = ชาวเกาะในพื้นที่ (Islander)</label>
                            <label class="form-check"><input type="radio" name="f1_residency" value="2"> 2 = นักท่องเที่ยวไทย (Thai tourist)</label>
                            <label class="form-check"><input type="radio" name="f1_residency" value="3"> 3 = นักท่องเที่ยวต่างชาติ (Foreigner)</label>
                            <label class="form-check"><input type="radio" name="f1_residency" value="4"> 4 = แรงงานข้ามชาติ (Migrant worker)</label>
                            <div style="margin-top: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>สัญชาติ:</span>
                                <input type="text" id="f1_nationality" style="width: 140px;">
                            </div>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ระดับความพิการเดิม<br>ก่อนป่วย<br>(Pre-morbid mRS: 0–5)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f1_premrs" value="0"> 0 = ปกติ ไม่มีอาการ</label>
                            <label class="form-check"><input type="radio" name="f1_premrs" value="1"> 1 = ไม่มีทุพพลภาพ ทำงานได้ปกติ</label>
                            <label class="form-check"><input type="radio" name="f1_premrs" value="2"> 2 = เล็กน้อย ดูแลตนเองได้</label>
                            <label class="form-check"><input type="radio" name="f1_premrs" value="3"> 3 = ปานกลาง เดินได้เอง</label>
                            <label class="form-check"><input type="radio" name="f1_premrs" value="4"> 4 = มาก ช่วยตนเองไม่ได้</label>
                            <label class="form-check"><input type="radio" name="f1_premrs" value="5"> 5 = นอนติดเตียง ต้องการดูแลตลอดเวลา</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">
                        <div>โรคร่วมสำคัญ</div>
                        <div>(Comorbidity by CCI)</div>
                        <div style="margin-top: 15px; font-size: 13px; color: #475569;">
                            <div>โปรแกรมคำนวณ:</div>
                            <div style="margin-top: 6px; padding: 6px; background: #ffffff; border: 1px solid #cbd5e1; display: inline-block; text-align: center; border-radius: 4px;">
                                <div style="font-size: 10px; font-weight: bold; color: #0284c7;">MDCalc CCI</div>
                                <div style="font-size: 10px; color: #64748b;">Auto Calculator</div>
                            </div>
                        </div>
                    </td>
                    <td colspan="3" style="background: #fafafa; padding: 12px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <!-- Column 1 -->
                            <div class="check-group">
                                <div>
                                    <label class="form-check" style="font-weight: 600;">
                                        <input type="checkbox" id="f1_cci_dm_chk" onchange="toggleCciDm(); calcCCI();"> Diabetes Mellitus (เบาหวาน)
                                    </label>
                                    <div id="f1_cci_dm_options" style="margin-left: 22px; margin-top: 3px; display: flex; gap: 12px;">
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_dm_type" value="1" onchange="calcCCI()"> ไม่มีภาวะแทรกซ้อน(+1)</label>
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_dm_type" value="2" onchange="calcCCI()"> มีภาวะแทรกซ้อน(+2)</label>
                                    </div>
                                </div>
                                <label class="form-check"><input type="checkbox" id="f1_cci_mi" value="1" onchange="calcCCI()"> Myocardial Infarction (โรคกล้ามเนื้อหัวใจตาย)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_chf" value="1" onchange="calcCCI()"> Congestive Heart Failure (โรคหัวใจล้มเหลว)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_pvd" value="1" onchange="calcCCI()"> Peripheral Vascular Disease (โรคหลอดเลือดส่วนปลาย)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_stroke" value="1" onchange="calcCCI()"> Prior Stroke/TIA (โรคเส้นเลือดสมองเดิม)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_hemi" value="2" onchange="calcCCI()"> Hemiplegia (มีภาวะอ่อนแรง)(+2)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_dementia" value="1" onchange="calcCCI()"> Dementia (โรคความจำเสื่อม)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_copd" value="1" onchange="calcCCI()"> Chronic Pulmonary Disease (โรคปอดเรื้อรัง)(+1)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_ctd" value="1" onchange="calcCCI()"> Connective Tissue Disease (โรคเนื้อเยื่อเกี่ยวพัน)(+1)</label>
                            </div>
                            <!-- Column 2 -->
                            <div class="check-group">
                                <label class="form-check"><input type="checkbox" id="f1_cci_pud" value="1" onchange="calcCCI()"> Peptic Ulcer Disease (โรคแผลทางเดินอาหาร)(+1)</label>
                                <div>
                                    <label class="form-check" style="font-weight: 600;">
                                        <input type="checkbox" id="f1_cci_liver_chk" onchange="toggleCciLiver(); calcCCI();"> Liver Disease (โรคทางตับ)
                                    </label>
                                    <div id="f1_cci_liver_options" style="margin-left: 22px; margin-top: 3px; display: flex; gap: 12px;">
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_liver_type" value="1" onchange="calcCCI()"> ไม่รุนแรง(+1)</label>
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_liver_type" value="3" onchange="calcCCI()"> ปานกลางถึงรุนแรงมาก(+3)</label>
                                    </div>
                                </div>
                                <label class="form-check"><input type="checkbox" id="f1_cci_ckd" value="2" onchange="calcCCI()"> CKD Stage 3-5 (ไตวายเรื้อรัง ระยะที่ 3-5)(+2)</label>
                                <div>
                                    <label class="form-check" style="font-weight: 600;">
                                        <input type="checkbox" id="f1_cci_tumor_chk" onchange="toggleCciTumor(); calcCCI();"> Solid Tumor (มะเร็งชนิดก้อน)
                                    </label>
                                    <div id="f1_cci_tumor_options" style="margin-left: 22px; margin-top: 3px; display: flex; gap: 12px;">
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_tumor_type" value="2" onchange="calcCCI()"> ไม่แพร่กระจาย(+2)</label>
                                        <label class="form-check" style="font-size: 14px;"><input type="radio" name="f1_cci_tumor_type" value="6" onchange="calcCCI()"> ระยะแพร่กระจาย(+6)</label>
                                    </div>
                                </div>
                                <label class="form-check"><input type="checkbox" id="f1_cci_leukemia" value="2" onchange="calcCCI()"> Leukemia (มะเร็งเม็ดเลือดขาว)(+2)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_lymphoma" value="2" onchange="calcCCI()"> Lymphoma (มะเร็งต่อมน้ำเหลือง)(+2)</label>
                                <label class="form-check"><input type="checkbox" id="f1_cci_aids" value="6" onchange="calcCCI()"> AIDS (ภาวะภูมิคุ้มกันบกพร่อง)(+6)</label>
                            </div>
                        </div>

                        <!-- Total CCI display -->
                        <div style="margin-top: 15px; padding-top: 10px; border-top: 2px dashed #cbd5e1; display: flex; justify-content: flex-end; align-items: center; gap: 10px;">
                            <span style="font-weight: 700; font-size: 16px; color: #1e3a8a;">รวมคะแนน CCI:</span>
                            <input type="text" id="f1_cci_total" class="input-calc" style="width: 90px; text-align: center; font-size: 18px;" readonly value="0">
                            <span style="font-weight: 700;">คะแนน</span>
                            <span style="font-size: 13px; color: #64748b;">(โรคร่วม: <span id="f1_cci_comorb_points">0</span> + อายุ: <span id="f1_cci_age_points">0</span>)</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">เวลาถึง ER เกาะลันตา (T0)</td>
                    <td>
                        <div style="display: flex; flex-direction: column; gap: 4px;">
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span>วันที่:</span><input type="date" id="f1_t0_date" onchange="syncT0(); calcTimelines();" oninput="syncT0(); calcTimelines();">
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span>เวลา:</span><input type="time" id="f1_t0_time" onchange="syncT0(); calcTimelines();" oninput="syncT0(); calcTimelines();"><span>น.</span>
                            </div>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">
                        <div>เวลาเริ่มมีอาการ</div>
                        <div>(Onset Time)</div>
                        <div style="margin-top: 6px; font-size: 13px; color: #1e3a8a;">ระยะเวลา Onset to ER</div>
                    </td>
                    <td>
                        <div style="display: flex; flex-direction: column; gap: 4px;">
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span>วันที่:</span><input type="date" id="f1_onset_date" onchange="calcTimelines();">
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span>เวลา(โดยประมาณ):</span><input type="time" id="f1_onset_time" onchange="calcTimelines();"><span>น.</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px; margin-top: 4px;">
                                <input type="text" id="f1_onset_to_er" class="input-calc" style="width: 90px; text-align: center;" readonly placeholder="--">
                                <span>นาที (Minutes)</span>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">รูปแบบการมา ER (Arrival Mode)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f1_arrival_mode" value="1"> 1 = รถพยาบาล 1669 , กู้ภัย (EMS)</label>
                            <label class="form-check"><input type="radio" name="f1_arrival_mode" value="2"> 2 = มาเอง / ญาติพามา (Walk-in)</label>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ระดับการคัดแยก (Triage ESI)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f1_esi" value="1"> ESI 1 (Resuscitation)</label>
                            <label class="form-check"><input type="radio" name="f1_esi" value="2"> ESI 2 (Emergent)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">
                        <div>ช่วงเวรการทำงาน (Island ED Shift)</div>
                        <div style="font-size: 11px; color: #0284c7; font-weight: normal; margin-top: 2px;">(Auto เลือกตามเวลา T1 ออกจากห้องฉุกเฉิน)</div>
                    </td>
                    <td colspan="3">
                        <div class="check-row">
                            <label class="form-check"><input type="radio" name="f1_shift" value="morning"> เวรเช้า (08:00–16:00 น.)</label>
                            <label class="form-check"><input type="radio" name="f1_shift" value="afternoon"> เวรบ่าย (16:00–24:00 น.)</label>
                            <label class="form-check"><input type="radio" name="f1_shift" value="night"> เวรดึก (00:00–08:00 น.)</label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 3 -->
        <div class="section-header">หมวดที่ 3: กลุ่มโรคเป้าหมายและความรุนแรงแรกรับจำเพาะโรค</div>
        <table class="crf-table">
            <tr id="sec3_row_stemi" class="disease-specific-row" data-disease="stemi">
                <td style="width: 32%; font-weight: 700; background: #f8fafc;">1. STEMI / Acute Coronary Syndrome</td>
                <td style="width: 68%;">
                    <div style="font-weight: 600; margin-bottom: 4px;">ระดับความรุนแรงภาวะหัวใจวายแรกรับ (Killip Severity):</div>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f1_killip" value="1" onchange="calcDeltaKillip()"> Killip Class I (No heart failure)</label>
                        <label class="form-check"><input type="radio" name="f1_killip" value="2" onchange="calcDeltaKillip()"> Killip Class II (Rales, S3 gallop, Mild Pulmonary edema)</label>
                        <label class="form-check"><input type="radio" name="f1_killip" value="3" onchange="calcDeltaKillip()"> Killip Class III (Severe Pulmonary edema)</label>
                        <label class="form-check"><input type="radio" name="f1_killip" value="4" onchange="calcDeltaKillip()"> Killip Class IV (Cardiogenic shock, Hypoperfusion sign)</label>
                    </div>
                </td>
            </tr>
            <tr id="sec3_row_ais" class="disease-specific-row" data-disease="ais">
                <td style="font-weight: 700; background: #f8fafc;">2. Acute Stroke</td>
                <td>
                    <div style="font-weight: 600; margin-bottom: 4px;">ระดับความรู้สึกตัวแรกรับ (Stroke Consciousness / GCS):</div>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f1_stroke_gcs" id="f1_stroke_gcs_1" value="severe"> GCS 3–8: Severe Coma (โคม่ารุนแรง)</label>
                        <label class="form-check"><input type="radio" name="f1_stroke_gcs" id="f1_stroke_gcs_2" value="moderate"> GCS 9–12: Moderate (ความรู้สึกตัวลดลงปานกลาง)</label>
                        <label class="form-check"><input type="radio" name="f1_stroke_gcs" id="f1_stroke_gcs_3" value="mild"> GCS 13–15: Mild (สับสนเล็กน้อยหรือรู้สึกตัวดี)</label>
                    </div>
                </td>
            </tr>
            <tr id="sec3_row_trauma" class="disease-specific-row" data-disease="trauma">
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">3. Severe Trauma (อุบัติเหตุบาดเจ็บรุนแรง)</td>
                <td>
                    <div style="font-weight: 600;">• กลไกการบาดเจ็บ (Injury Mechanism):</div>
                    <div class="check-group" style="margin-left: 15px; margin-top: 3px; margin-bottom: 8px;">
                        <label class="form-check"><input type="checkbox" id="f1_trauma_mech1"> High-velocity traffic collision (อุบัติเหตุจราจรความเร็วสูง)</label>
                        <label class="form-check"><input type="checkbox" id="f1_trauma_mech2"> Fall from height (ตกจากที่สูง)</label>
                        <label class="form-check"><input type="checkbox" id="f1_trauma_mech3"> Penetrating trauma (บาดแผลถูกแทง/ยิง)</label>
                    </div>
                    <div style="font-weight: 600;">• คะแนนสรีรวิทยาการบาดเจ็บ (Physiological Trauma Acuity):</div>
                    <div class="check-group" style="margin-left: 15px; margin-top: 3px;">
                        <label class="form-check"><input type="radio" name="f1_trauma_acuity" id="f1_trauma_acuity_crit" value="critical"> RTS &lt;= 6: Critical physiological acuity (วิกฤต)</label>
                        <label class="form-check"><input type="radio" name="f1_trauma_acuity" id="f1_trauma_acuity_mod" value="moderate"> RTS &gt; 6: Moderate physiological acuity (ปานกลาง)</label>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 4 -->
        <div class="section-header">หมวดที่ 4: สัญญาณชีพและผลตรวจทางห้องปฏิบัติการแรกรับ ณ รพ.เกาะลันตา</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 25%;">ตัวชี้วัดแรกรับ (Vital Sign)</th>
                    <th style="width: 25%;">ค่าแรกรับ</th>
                    <th style="width: 25%;">ตัวชี้วัดแรกรับ (Vital Sign)</th>
                    <th style="width: 25%;">ค่าแรกรับ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">ความดันโลหิตซิสโตลิก (SBP)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_sbp" style="width: 90px;" oninput="calcVitals()">
                            <span>mmHg</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ความดันโลหิตไดแอสโตลิก (DBP)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_dbp" style="width: 90px;" oninput="calcVitals()">
                            <span>mmHg</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">
                        <div>ความดันโลหิตเฉลี่ย (MAP)</div>
                        <div style="font-size: 12px; color: #64748b;">(สูตร: [SBP + 2*DBP] / 3)</div>
                    </td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="text" id="f1_map" class="input-calc" style="width: 90px; text-align: center;" readonly placeholder="--">
                            <span>mmHg</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">อัตราการเต้นของหัวใจ (HR)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_hr" style="width: 90px;" oninput="calcVitals()">
                            <span>ครั้ง/นาที (bpm)</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">อัตราการหายใจ (RR)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_rr" style="width: 90px;" oninput="calcVitals()">
                            <span>ครั้ง/นาที</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ความอิ่มตัวออกซิเจน (O2Sat / SpO2)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <input type="number" id="f1_spo2" style="width: 70px;">
                            <span>%</span>
                            <label class="form-check" style="font-size: 13px;"><input type="radio" name="f1_o2support" value="ra"> Room Air</label>
                            <label class="form-check" style="font-size: 13px;"><input type="radio" name="f1_o2support" value="o2"> O2 Support</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">อุณหภูมิกายแรกรับ (Body Temp: BT)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_bt" step="0.1" style="width: 80px;" oninput="calcDeltaBT()">
                            <span>°C</span>
                        </div>
                    </td>
                    <td id="f1_label_hct" style="font-weight: 700; background: #f8fafc;">
                        ความเข้มข้นของเลือดแรกรับ (Baseline Hct)
                        <div style="font-size: 11px; color: #64748b; font-weight: normal;">(เฉพาะผู้ป่วย Trauma)</div>
                    </td>
                    <td id="f1_cell_hct">
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f1_hct" step="0.1" style="width: 80px;" placeholder="N/A" disabled>
                            <span>%</span>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 5 -->
        <div class="section-header">หมวดที่ 5: คะแนนความรุนแรงทางสรีรวิทยาและดัชนีการไหลเวียนเลือดแรกรับ</div>
        <table class="crf-table">
            <tr id="sec5_row_msi" class="disease-specific-row" data-disease="stemi">
                <td style="width: 32%; font-weight: 700; background: #f8fafc;">
                    Modified Shock Index
                    <div style="font-size: 11px; color: #64748b; font-weight: normal;">(คำนวณเฉพาะผู้ป่วย STEMI)</div>
                </td>
                <td style="width: 68%;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>ค่าที่คำนวณได้:</span>
                        <input type="text" id="f1_msi" class="input-calc" style="width: 100px; text-align: center;" readonly placeholder="--">
                        <span style="font-size: 13px; color: #64748b;">(สูตร: MSI = HR / MAP)</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">คะแนนความรู้สึกตัวรวม (Total GCS)</td>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <span>E</span><input type="number" id="f1_gcs_e" min="1" max="4" style="width: 50px;" oninput="calcGCS()">
                        <span>V</span><input type="number" id="f1_gcs_v" min="1" max="5" style="width: 50px;" oninput="calcGCS()">
                        <span>M</span><input type="number" id="f1_gcs_m" min="1" max="6" style="width: 50px;" oninput="calcGCS()">
                        <span style="margin-left: 10px; font-weight: 700;">รวม:</span>
                        <input type="text" id="f1_gcs_total" class="input-calc" style="width: 70px; text-align: center;" readonly placeholder="--">
                        <span>คะแนน (3–15)</span>
                    </div>
                </td>
            </tr>
            <tr id="sec5_row_rts" class="disease-specific-row" data-disease="trauma">
                <td style="font-weight: 700; background: #f8fafc;">
                    คะแนนการบาดเจ็บรวม (Total RTS Score)
                    <div style="font-size: 11px; color: #dc2626; font-weight: normal;">(คำนวณเฉพาะผู้ป่วย Trauma)</div>
                </td>
                <td>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span>คะแนน RTS รวม:</span>
                            <input type="text" id="f1_rts_total" class="input-calc" style="width: 100px; text-align: center;" readonly placeholder="--">
                            <span>(ช่วงคะแนน 0–7.841)</span>
                        </div>
                        <div style="font-size: 12px; color: #64748b;">
                            (สูตร: RTS = 0.9368 GCS + 0.7326 SBP + 0.2908 RR)
                        </div>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 6 -->
        <div class="section-header">หมวดที่ 6: การกู้ชีพและการเตรียมพร้อมก่อนส่งต่อ ณ รพ.เกาะลันตา</div>
        <table class="crf-table">
            <tr>
                <td style="width: 32%; font-weight: 700; background: #f8fafc;">การใส่ท่อช่วยหายใจ (Pre-Transfer Intubation)</td>
                <td style="width: 68%;">
                    <div class="check-row">
                        <label class="form-check"><input type="radio" name="f1_intubation" value="0" onchange="toggleIntubationDetails()"> ไม่ได้ใส่</label>
                        <label class="form-check"><input type="radio" name="f1_intubation" value="1" onchange="toggleIntubationDetails()"> ใส่ท่อช่วยหายใจตั้งแต่ รพ.เกาะลันตา</label>
                    </div>
                    <div id="f1_ett_details_box" style="margin-left: 20px; margin-top: 6px; display: flex; align-items: center; gap: 8px; opacity: 0.35; pointer-events: none; transition: all 0.2s ease;">
                        <span>(ETT No.</span><input type="text" id="f1_ett_no" style="width: 65px; background-color: #f1f5f9;" placeholder="เช่น 7.5" disabled>
                        <span>, เวลาใส่:</span><input type="time" id="f1_ett_time" style="background-color: #f1f5f9;" disabled><span>น.)</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">การให้ยากระตุ้นความดัน (Pre-Transfer Inotropes)</td>
                <td>
                    <div class="check-row">
                        <label class="form-check"><input type="radio" name="f1_inotropes" value="0" onchange="toggleInotropesDetails()"> ไม่ได้รับ</label>
                        <label class="form-check"><input type="radio" name="f1_inotropes" value="1" onchange="toggleInotropesDetails()"> ได้รับยากระตุ้นความดัน</label>
                    </div>
                    <div id="f1_inotropes_details_box" style="margin-left: 20px; margin-top: 6px; display: flex; align-items: center; gap: 8px; opacity: 0.35; pointer-events: none; transition: all 0.2s ease;">
                        <span>(ระบุยา:</span><input type="text" id="f1_inotropes_name" style="width: 140px; background-color: #f1f5f9;" placeholder="เช่น Norepinephrine" disabled>
                        <span>, ขนาดยา:</span><input type="text" id="f1_inotropes_dose" style="width: 140px; background-color: #f1f5f9;" placeholder="เช่น 0.1 mcg/kg/min" disabled><span>)</span>
                    </div>
                </td>
            </tr>
            <tr id="sec6_row_trauma_resusc" class="disease-specific-row" data-disease="trauma">
                <td style="font-weight: 700; background: #f8fafc;">
                    การกู้ชีพผู้ป่วยบาดเจ็บ (Trauma Resuscitation)
                    <div style="font-size: 11px; color: #dc2626; font-weight: normal;">(เฉพาะผู้ป่วย Trauma)</div>
                </td>
                <td>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                        <label class="form-check"><input type="checkbox" id="f1_resusc_txa"> ให้ยา Tranexamic Acid (TXA)</label>
                        <label class="form-check"><input type="checkbox" id="f1_resusc_splint"> ดามกระดูก (Splinting)</label>
                        <label class="form-check"><input type="checkbox" id="f1_resusc_pelvic"> ใส่สายรัดเชิงกราน (Pelvic binder)</label>
                        <label class="form-check"><input type="checkbox" id="f1_resusc_icd"> ใส่ท่อระบายทรวงอก (Chest Tube)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>เวลาแพทย์สั่งส่งต่อ / ออกจาก ER</div>
                    <div>(T1: ER Door-Out)</div>
                </td>
                <td>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f1_t1_date" onchange="syncT1(); calcTimelines();" oninput="syncT1(); calcTimelines();">
                        <span>เวลา:</span><input type="time" id="f1_t1_time" onchange="syncT1(); calcTimelines();" oninput="syncT1(); calcTimelines();"><span>น.</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>T0-1: Island ED DIDO Delay</div>
                    <div style="font-size: 13px; color: #64748b;">(T1 - T0)</div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span>เวลาที่คำนวณได้:</span>
                        <input type="text" id="f1_dido_min" class="input-calc" style="width: 90px; text-align: center;" readonly placeholder="--">
                        <span style="font-weight: 700;">นาที</span>
                    </div>
                    <div style="font-size: 13px; color: #475569; margin-bottom: 6px;">
                        • เกณฑ์ปกติ Stroke / STEMI: &lt;= 45 นาที (ล่าช้าเมื่อ &gt; 45 นาที)<br>
                        • เกณฑ์ปกติ Severe Trauma: &lt;= 60 นาที (ล่าช้าเมื่อ &gt; 60 นาที)
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; padding-top: 4px;">
                        <span style="font-weight: 700;">การประเมิน:</span>
                        <label class="form-check" style="font-weight: 600; color: #166534;"><input type="radio" name="f1_dido_eval" id="f1_dido_ontime" value="ontime"> ทัน</label>
                        <label class="form-check" style="font-weight: 600; color: #991b1b;"><input type="radio" name="f1_dido_eval" id="f1_dido_delay" value="delay"> ล่าช้า (DIDO Delay Breach)</label>
                    </div>
                </td>
            </tr>
        </table>
        </div> <!-- End of f1_post_screening_container -->

    </div>
    """
