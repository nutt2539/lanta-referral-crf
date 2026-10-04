# -*- coding: utf-8 -*-
"""
Form 4 HTML Generator module
"""

def get_form4_html():
    return """
    <div id="page-form4" class="crf-page theme-form4">
        <!-- Header Box -->
        <div class="doc-header-box">
            <h2>แบบบันทึกข้อมูลการวิจัยทางคลินิก (CASE RECORD FORM: CRF)</h2>
            <h3>ส่วนที่ 4: การรักษา สรีรวิทยาเปรียบเทียบ และผลลัพธ์ทางคลินิกระยะแรก ณ รพ.กระบี่</h3>
            <p>Form 4: Mainland Definitive Care, Physiological Changes & Early Clinical Outcomes</p>
        </div>

        <!-- Table 1: Identifiers -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">รหัสวิจัยผู้ป่วย (STUDY_ID)</td>
                <td style="width: 25%;">
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span>LANTA_</span>
                        <input type="text" id="f4_study_id" class="study-id-sync" placeholder="เช่น 001" style="font-weight: 700; color: #1e3a8a;">
                    </div>
                </td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เลขที่ใบส่งต่อ (Refer_ID)</td>
                <td style="width: 25%;">
                    <input type="text" id="f4_refer_id" class="refer-id-sync" placeholder="ระบุเลขที่ใบส่งต่อ">
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">เลขประจำตัวผู้ป่วย (HN / VN เกาะลันตา)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>HN:</span><input type="text" id="f4_hn" class="hn-sync" style="width: 80px;">
                        <span>VN:</span><input type="text" id="f4_vn" class="vn-sync" style="width: 80px;">
                    </div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">วันที่สกัดข้อมูล / ผู้สกัด (Abstractor)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f4_abs_date" class="date-sync" style="width: 125px;">
                        <span>ผู้สกัด:</span><input type="text" id="f4_abstractor" class="abs-sync" style="width: 100px;">
                    </div>
                </td>
            </tr>
        </table>

        <!-- Table 2: Mainland ER Context -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เลขที่เวชระเบียน รพ.กระบี่ (HN)</td>
                <td style="width: 25%;"><input type="text" id="f4_krabi_hn" placeholder="HN รพ.กระบี่"></td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เวลาถึง ER รพ.กระบี่ (T4)</td>
                <td style="width: 25%;">
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f4_t4_date" onchange="syncT4_fromF4(); calcForm4Timelines();" style="width: 125px;">
                        <span>เวลา:</span><input type="time" id="f4_t4_time" onchange="syncT4_fromF4(); calcForm4Timelines();" oninput="syncT4_fromF4(); calcForm4Timelines();"><span>น.</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">หอผู้ป่วยรับไว้รักษาแรกรับ</td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f4_ward" value="ccu"> CCU (Coronary Care)</label>
                        <label class="form-check"><input type="radio" name="f4_ward" value="stroke"> Stroke Unit</label>
                        <label class="form-check"><input type="radio" name="f4_ward" value="sicu"> Trauma ICU / SICU</label>
                        <label class="form-check"><input type="radio" name="f4_ward" value="general"> หอผู้ป่วยสามัญ</label>
                    </div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">แพทย์ผู้รับผิดชอบการรักษา</td>
                <td><input type="text" id="f4_physician" placeholder="ชื่อ-สกุล แพทย์เจ้าของไข้"></td>
            </tr>
        </table>

        <!-- หมวดที่ 1 -->
        <div class="section-header">หมวดที่ 1: สัญญาณชีพและความรุนแรงแรกรับ ณ ER รพ.กระบี่</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 25%;">ตัวชี้วัดแรกรับ (Krabi ED)</th>
                    <th style="width: 25%;">ค่าที่วัดได้</th>
                    <th style="width: 25%;">ตัวชี้วัดแรกรับ (Krabi ED)</th>
                    <th style="width: 25%;">ค่าที่วัดได้</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">ความดันโลหิตซิสโตลิก (SBP_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_sbp" style="width: 90px;" oninput="calcKrabiVitals()">
                            <span>mmHg</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ความดันโลหิตไดแอสโตลิก (DBP_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_dbp" style="width: 90px;" oninput="calcKrabiVitals()">
                            <span>mmHg</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">
                        <div>ความดันโลหิตเฉลี่ย (MAP_Krabi)</div>
                        <div style="font-size: 12px; color: #64748b;">([SBP + 2*DBP] / 3)</div>
                    </td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="text" id="f4_map" class="input-calc" style="width: 90px; text-align: center;" readonly placeholder="--">
                            <span>mmHg</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">อัตราการเต้นของหัวใจ (HR_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_hr" style="width: 90px;" oninput="calcKrabiVitals()">
                            <span>ครั้ง/นาที (bpm)</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">อัตราการหายใจ (RR_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_rr" style="width: 90px;" oninput="calcKrabiVitals()">
                            <span>ครั้ง/นาที</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ความอิ่มตัวออกซิเจน (O2Sat_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_spo2" style="width: 80px;">
                            <span>%</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">อุณหภูมิกายแรกรับ (BT_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_bt" step="0.1" style="width: 80px;" oninput="calcDeltaBT()">
                            <span>°C</span>
                        </div>
                    </td>
                    <td style="font-weight: 700; background: #f8fafc;">ความเข้มข้นเลือด (Hct_Krabi)</td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <input type="number" id="f4_hct" step="0.1" style="width: 80px;">
                            <span>%</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">
                        ระดับความรู้สึกตัวแรกรับ (GCS_Krabi)
                        <div style="font-size: 11px; color: #64748b; font-weight: normal;">(Glasgow Coma Scale: E + V + M)</div>
                    </td>
                    <td colspan="3">
                        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span style="font-weight: 600;">E:</span>
                                <input type="number" id="f4_gcs_e" min="1" max="4" style="width: 50px;" oninput="calcKrabiGCS()" placeholder="1-4">
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span style="font-weight: 600;">V:</span>
                                <input type="number" id="f4_gcs_v" min="1" max="5" style="width: 50px;" oninput="calcKrabiGCS()" placeholder="1-5">
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span style="font-weight: 600;">M:</span>
                                <input type="number" id="f4_gcs_m" min="1" max="6" style="width: 50px;" oninput="calcKrabiGCS()" placeholder="1-6">
                            </div>
                            <div style="display: flex; align-items: center; gap: 4px; margin-left: 10px;">
                                <span style="font-weight: 700; color: #1e3a8a;">คะแนนรวม (Total GCS):</span>
                                <input type="text" id="f4_gcs_total" class="input-calc" style="width: 65px; text-align: center; font-weight: 700;" readonly placeholder="--">
                                <span>/ 15</span>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td id="f4_cell_killip_lbl" style="font-weight: 700; background: #f8fafc;">
                        STEMI Killip Class ณ รพ.กระบี่
                        <div style="font-size: 11px; color: #0284c7; font-weight: normal;">(เฉพาะผู้ป่วย STEMI)</div>
                    </td>
                    <td id="f4_cell_killip_val">
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_killip" value="1_2" onchange="calcDeltaKillip()"> Killip Class I,II</label>
                            <label class="form-check"><input type="radio" name="f4_killip" value="3" onchange="calcDeltaKillip()"> Killip Class III</label>
                            <label class="form-check"><input type="radio" name="f4_killip" value="4" onchange="calcDeltaKillip()"> Killip Class IV</label>
                        </div>
                    </td>
                    <td id="f4_cell_stroke_lbl" style="font-weight: 700; background: #f8fafc;">
                        Stroke GCS Consciousness
                        <div style="font-size: 11px; color: #7c3aed; font-weight: normal;">(เฉพาะผู้ป่วย Stroke)</div>
                    </td>
                    <td id="f4_cell_stroke_val">
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_stroke_gcs" id="f4_stroke_gcs_1" value="severe"> GCS 3–8 (Severe Coma)</label>
                            <label class="form-check"><input type="radio" name="f4_stroke_gcs" id="f4_stroke_gcs_2" value="moderate"> GCS 9–12 (Moderate)</label>
                            <label class="form-check"><input type="radio" name="f4_stroke_gcs" id="f4_stroke_gcs_3" value="mild"> GCS 13–15 (Mild)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td id="f4_cell_trauma_lbl" style="font-weight: 700; background: #f8fafc;">
                        Trauma Acuity (RTS_Krabi)
                        <div style="font-size: 11px; color: #dc2626; font-weight: normal;">(เฉพาะผู้ป่วย Trauma)</div>
                    </td>
                    <td id="f4_cell_trauma_val">
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_trauma_acuity" id="f4_trauma_crit" value="critical"> RTS &lt;= 6 (Critical)</label>
                            <label class="form-check"><input type="radio" name="f4_trauma_acuity" id="f4_trauma_mod" value="moderate"> RTS &gt; 6 (Moderate)</label>
                        </div>
                    </td>
                    <td id="f4_cell_msi_lbl" style="font-weight: 700; background: #f8fafc;">
                        Modified Shock Index
                        <div style="font-size: 11px; color: #0284c7; font-weight: normal;">(คำนวณเฉพาะ STEMI)</div>
                    </td>
                    <td id="f4_cell_msi_val">
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <span>คำนวณ (HR/MAP):</span>
                            <input type="text" id="f4_msi" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 2 -->
        <div class="section-header">หมวดที่ 2: การคำนวณการเปลี่ยนแปลงสรีรวิทยาระหว่างการส่งต่อ (เกาะลันตา vs. กระบี่)</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 25%;">ตัวแปรการเปลี่ยนแปลง (Delta Metric)</th>
                    <th style="width: 25%;">สูตรการคำนวณเปรียบเทียบ</th>
                    <th style="width: 25%; text-align: center;">ผลต่างที่คำนวณได้</th>
                    <th style="width: 25%;">การประเมินภาวะทรุดหนัก</th>
                </tr>
            </thead>
            <tbody>
                <tr id="f4_row_delta_killip" class="disease-specific-row" data-disease="stemi">
                    <td style="font-weight: 700; background: #f8fafc;">ΔKillip Class (STEMI Severity)</td>
                    <td>Killip_Krabi - Killip_Lanta</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <span>จาก Class</span>
                            <input type="text" id="f4_delta_killip_from" class="input-calc" style="width: 40px; text-align: center;" readonly placeholder="-">
                            <span>สู่</span>
                            <input type="text" id="f4_delta_killip_to" class="input-calc" style="width: 40px; text-align: center;" readonly placeholder="-">
                        </div>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_killip" id="f4_killip_stable" value="stable"> คงที่ / ดีขึ้น</label>
                            <label class="form-check"><input type="radio" name="f4_eval_killip" id="f4_killip_deter" value="deter"> ทรุดหนัก (ΔKillip &gt;= +1 หรือดำเนินสู่ Class IV)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">ΔGCS (Neurological Status)</td>
                    <td>GCS_Krabi - GCS_Lanta</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f4_delta_gcs" class="input-calc" style="width: 70px; text-align: center;" readonly placeholder="--">
                            <span>คะแนน</span>
                        </div>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_gcs" id="f4_gcs_stable" value="stable"> คงที่ / ดีขึ้น</label>
                            <label class="form-check"><input type="radio" name="f4_eval_gcs" id="f4_gcs_deter" value="deter"> ทรุดหนัก (ΔGCS &lt;= -2)</label>
                        </div>
                    </td>
                </tr>
                <tr id="f4_row_delta_rts" class="disease-specific-row" data-disease="trauma">
                    <td style="font-weight: 700; background: #f8fafc;">ΔRTS (Trauma Acuity)</td>
                    <td>RTS_Krabi - RTS_Lanta</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f4_delta_rts" class="input-calc" style="width: 70px; text-align: center;" readonly placeholder="--">
                            <span>คะแนน</span>
                        </div>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_rts" id="f4_rts_stable" value="stable"> คงที่ / ดีขึ้น</label>
                            <label class="form-check"><input type="radio" name="f4_eval_rts" id="f4_rts_deter" value="deter"> ทรุดหนัก (ΔRTS &lt;= -1.0)</label>
                        </div>
                    </td>
                </tr>
                <tr id="f4_row_delta_msi" class="disease-specific-row" data-disease="stemi">
                    <td style="font-weight: 700; background: #f8fafc;">
                        ΔModified Shock Index (ΔMSI)
                        <div style="font-size: 11px; color: #0284c7; font-weight: normal;">(คำนวณเฉพาะผู้ป่วย STEMI)</div>
                    </td>
                    <td>MSI_Krabi - MSI_Lanta</td>
                    <td class="td-center">
                        <input type="text" id="f4_delta_msi" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_msi" id="f4_msi_stable" value="stable"> คงที่ / ปกติ</label>
                            <label class="form-check"><input type="radio" name="f4_eval_msi" id="f4_msi_deter" value="deter"> ทรุดหนัก (ΔMSI &gt;= +0.15)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">ΔMAP (Hemodynamic Change)</td>
                    <td>MAP_Krabi - MAP_Lanta</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f4_delta_map" class="input-calc" style="width: 70px; text-align: center;" readonly placeholder="--">
                            <span>mmHg</span>
                        </div>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_map" id="f4_map_stable" value="stable"> คงที่ (MAP เพิ่มขึ้นหรือ &gt;= 65 mmHg)</label>
                            <label class="form-check"><input type="radio" name="f4_eval_map" id="f4_map_deter" value="deter"> ทรุดหนัก (MAP ลดลง และ &lt; 65 mmHg)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">ΔBody Temperature (ΔBT)</td>
                    <td>BT_Krabi - BT_Lanta</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f4_delta_bt" class="input-calc" style="width: 70px; text-align: center;" readonly placeholder="--">
                            <span>°C</span>
                        </div>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f4_eval_bt" id="f4_bt_normal" value="normal"> ปกติ</label>
                            <label class="form-check"><input type="radio" name="f4_eval_bt" id="f4_bt_hypo" value="hypothermia"> เกิด Hypothermia (&lt; 35 °C)</label>
                        </div>
                    </td>
                </tr>
                <tr style="background: #f1f5f9;">
                    <td style="font-weight: 700; color: #1e3a8a;">
                        สรุปภาวะทรุดหนักสรีรวิทยารวม
                    </td>
                    <td colspan="2" style="font-size: 13px; color: #475569;">
                        เพิ่มนิยาม: In-transit CPR/ETT/Inotrope*<br>
                        <span style="font-size: 12px; color: #64748b;">*เปิดใช้ยาใหม่ หรือเพิ่มขนาดยาเดิมขึ้น≥50%</span>
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check" style="font-weight: 700; color: #166534;">
                                <input type="radio" name="f4_composite_deter" id="f4_deter_stable" value="0"> 0 = สัญญาณชีพคงที่ตลอดการส่งต่อ (Stable)
                            </label>
                            <label class="form-check" style="font-weight: 700; color: #991b1b;">
                                <input type="radio" name="f4_composite_deter" id="f4_deter_event" value="1"> 1 = เกิดภาวะทรุด (Deteriorated)
                            </label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 3 -->
        <div class="section-header">หมวดที่ 3: การรักษาและกรอบเวลา ณ รพ.กระบี่</div>
        <table class="crf-table">
            <tr>
                <td style="width: 32%; font-weight: 700; background: #f8fafc;">
                    <div>วันและเวลาเริ่มทำหัตถการรักษาจำเพาะ (T5)</div>
                    <div style="font-size: 11px; color: #2563eb; font-weight: normal;">(🔗 ลิ้งค์ข้อมูลอัตโนมัติกับ Form 2: T5 Definitive Management)</div>
                </td>
                <td style="width: 68%;">
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f4_t5_date" onchange="syncT5_fromF4();" oninput="syncT5_fromF4();" style="width: 125px;">
                        <span>เวลา:</span><input type="time" id="f4_t5_time" onchange="syncT5_fromF4();" oninput="syncT5_fromF4();"><span>น.</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">ระยะเวลา Door-to-Intervention รพ.กระบี่ (T4-5)</td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span>คำนวณ: T5 - T4 =</span>
                        <input type="text" id="f4_t4_5_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                        <span>นาที</span>
                    </div>
                </td>
            </tr>
            <tr id="f4_row_golden_stemi" class="disease-specific-row" data-disease="stemi">
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">1. STEMI / ACS: Primary PCI</td>
                <td>
                    <div class="check-group">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span>• เวลาสายลวดผ่านรอยโรคใน Cath Lab (Primary PCI Wire Crossing):</span>
                            <input type="time" id="f4_pci_wire_time" onchange="syncT5_fromIntervention('stemi'); calcGoldenWindows();" oninput="syncT5_fromIntervention('stemi'); calcGoldenWindows();"><span>น.</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; margin-top: 3px;">
                            <span>• เวลารวม Door-to-Balloon นับจาก First Medical Contact เกาะลันตา:</span>
                            <input type="text" id="f4_pci_d2b_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                        <div style="margin-top: 5px;">
                            <div style="font-weight: 600;">• การบรรลุเกณฑ์ Golden Window Remote Primary PCI:</div>
                            <div class="check-group" style="margin-left: 15px; margin-top: 3px;">
                                <label class="form-check" style="color: #166534; font-weight: 600;">
                                    <input type="radio" name="f4_eval_pci" id="f4_pci_achieved" value="achieved"> บรรลุเกณฑ์ Remote Primary PCI (&lt;= 180 นาที ตามเกณฑ์ ESC Extended Reperfusion)
                                </label>
                                <label class="form-check" style="color: #991b1b; font-weight: 600;">
                                    <input type="radio" name="f4_eval_pci" id="f4_pci_missed" value="missed"> หลุดกรอบเวลา (STEMI PCI &gt; 180 นาที)
                                </label>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            <tr id="f4_row_golden_ais" class="disease-specific-row" data-disease="ais">
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">2. Acute Ischemic Stroke: Reperfusion Therapy</td>
                <td>
                    <div class="check-group">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span>• เวลาเริ่มฉีดยาละลายลิ่มเลือด (IV rtPA Bolus):</span>
                            <input type="time" id="f4_rtpa_time" onchange="syncT5_fromIntervention('ais'); calcGoldenWindows();" oninput="syncT5_fromIntervention('ais'); calcGoldenWindows();"><span>น.</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; margin-top: 3px;">
                            <span>• เวลาทำ CT Brain เสร็จสิ้น (CT Brain Completion):</span>
                            <input type="time" id="f4_ct_brain_time"><span>น.</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; margin-top: 3px;">
                            <span>• เวลารวม Onset-to-Needle (นับจากเริ่มมีอาการจนถึงเริ่มฉีด rtPA):</span>
                            <input type="text" id="f4_stroke_o2n_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                        <div style="margin-top: 5px;">
                            <div style="font-weight: 600;">• การบรรลุเกณฑ์ Golden Window IV rtPA:</div>
                            <div class="check-group" style="margin-left: 15px; margin-top: 3px;">
                                <label class="form-check" style="color: #166534; font-weight: 600;">
                                    <input type="radio" name="f4_eval_stroke" id="f4_stroke_achieved" value="achieved"> บรรลุเกณฑ์ IV rtPA (&lt;= 4.5 ชั่วโมง)
                                </label>
                                <label class="form-check" style="color: #991b1b; font-weight: 600;">
                                    <input type="radio" name="f4_eval_stroke" id="f4_stroke_missed" value="missed"> หลุดกรอบเวลา (Stroke rtPA &gt; 4.5 ชั่วโมง)
                                </label>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            <tr id="f4_row_golden_trauma" class="disease-specific-row" data-disease="trauma">
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">3. Severe Trauma: Definitive Management</td>
                <td>
                    <div class="check-group" style="display: flex; flex-direction: column; gap: 8px;">
                        <!-- CT Scan Section -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <span style="font-weight: 600; color: #1e293b;">• เวลาทำ CT Scan เสร็จสิ้น (CT Completion Time):</span>
                                <input type="time" id="f4_trauma_ct_time" onchange="syncT5_fromIntervention('trauma_ct'); calcGoldenWindows();" oninput="syncT5_fromIntervention('trauma_ct'); calcGoldenWindows();">
                                <span>น.</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-top: 5px; font-size: 13px; color: #475569;">
                                <span>เวลารวม Door-to-CT (นับจาก T0 เกาะลันตา):</span>
                                <input type="text" id="f4_trauma_d2ct_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                                <span style="font-weight: 600;">นาที</span>
                                <span style="font-size: 12px; color: #64748b;">(เกณฑ์เป้าหมาย &lt;= 150 นาที)</span>
                            </div>
                        </div>

                        <!-- OR Section -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <span style="font-weight: 600; color: #1e293b;">• เวลาลงมีดผ่าตัดฉุกเฉินระงับการเสียเลือด (Damage Control OR Incision):</span>
                                <input type="time" id="f4_or_time" onchange="syncT5_fromIntervention('trauma_or'); calcGoldenWindows();" oninput="syncT5_fromIntervention('trauma_or'); calcGoldenWindows();">
                                <span>น.</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-top: 5px; font-size: 13px; color: #475569;">
                                <span>เวลารวม Door-to-OR (นับจาก T0 เกาะลันตา):</span>
                                <input type="text" id="f4_trauma_d2or_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                                <span style="font-weight: 600;">นาที</span>
                                <span style="font-size: 12px; color: #64748b;">(เกณฑ์เป้าหมาย &lt;= 180 นาที)</span>
                            </div>
                        </div>

                        <!-- Evaluation Section -->
                        <div style="margin-top: 2px;">
                            <div style="font-weight: 600; color: #1e293b;">• การบรรลุเกณฑ์ Golden Window Definitive Management (CT / Emergent OR):</div>
                            <div class="check-group" style="margin-left: 15px; margin-top: 4px;">
                                <label class="form-check" style="color: #166534; font-weight: 600;">
                                    <input type="radio" name="f4_eval_trauma" id="f4_trauma_achieved" value="achieved"> บรรลุเกณฑ์ตามเวลา (Emergent OR &lt;= 180 นาที หรือ CT &lt;= 150 นาที)
                                </label>
                                <label class="form-check" style="color: #991b1b; font-weight: 600;">
                                    <input type="radio" name="f4_eval_trauma" id="f4_trauma_missed" value="missed"> หลุดกรอบเวลา (Trauma OR &gt; 180 นาที หรือ Trauma CT &gt; 150 นาที)
                                </label>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 4 -->
        <div class="section-header">หมวดที่ 4: ผลลัพธ์การเสียชีวิตระยะแรกและการรอดชีวิต ณ รพ.กระบี่</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    <div>1. การเสียชีวิตทันที ณ ห้องฉุกเฉิน รพ.กระบี่</div>
                    <div style="font-size: 13px; color: #64748b;">(MORT_ER_KBH)</div>
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f4_mort_er" value="0" onchange="toggleMortalityDetails()"> 0 = รอดชีวิตผ่านพ้นห้องฉุกเฉินและรับไว้รักษาต่อในหอผู้ป่วย</label>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <label class="form-check"><input type="radio" name="f4_mort_er" value="1" onchange="toggleMortalityDetails()"> 1 = เสียชีวิตทันที ณ ห้องฉุกเฉิน รพ.กระบี่</label>
                            <span>• เวลาเสียชีวิต:</span><input type="time" id="f4_mort_er_time" disabled><span>น.</span>
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>2. การเสียชีวิตภายใน 24 ชม. แรกหลังรับไว้รักษา</div>
                    <div style="font-size: 13px; color: #64748b;">(MORT_24H_POST)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f4_mort_24h" value="0" onchange="toggleMortalityDetails()"> 0 = รอดชีวิตเกิน 24 ชั่วโมงแรกหลังรับไว้รักษาใน รพ.กระบี่</label>
                        <div>
                            <label class="form-check"><input type="radio" name="f4_mort_24h" value="1" onchange="toggleMortalityDetails()"> 1 = เสียชีวิตภายใน 24 ชั่วโมงแรกหลังรับไว้รักษา (Subsequent 24-hr In-Hospital Death)</label>
                            <div style="margin-left: 22px; margin-top: 4px; display: flex; align-items: center; gap: 8px;">
                                <span>• วันที่เสียชีวิต:</span><input type="date" id="f4_mort_24h_date" style="width: 125px;" disabled>
                                <span>เวลา:</span><input type="time" id="f4_mort_24h_time" disabled><span>น.</span>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">
                    <div>3. สาเหตุการเสียชีวิตหลัก</div>
                    <div style="font-size: 13px; color: #64748b;">(Primary Cause of Death)</div>
                    <div style="font-size: 11px; color: #ef4444; font-weight: normal;">(ระบุได้เฉพาะกรณีผู้ป่วยเสียชีวิต)</div>
                </td>
                <td>
                    <div id="f4_mort_cause_container" class="check-group" style="opacity: 0.35; pointer-events: none;">
                        <label class="form-check"><input type="radio" name="f4_mort_cause" value="stemi" disabled> Cardiogenic shock / Malignant ventricular arrhythmia (STEMI)</label>
                        <label class="form-check"><input type="radio" name="f4_mort_cause" value="stroke" disabled> Massive cerebral infarction / Brain herniation (Ischemic Stroke)</label>
                        <label class="form-check"><input type="radio" name="f4_mort_cause" value="trauma" disabled> Exsanguinating hemorrhagic shock / Coagulopathy (Severe Trauma)</label>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <label class="form-check"><input type="radio" name="f4_mort_cause" value="other" disabled> อื่นๆ ระบุ (ICD-10):</label>
                            <input type="text" id="f4_mort_cause_icd" style="width: 200px;" disabled>
                        </div>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดประเมินสรุปทางระบาดวิทยาและคอขวดเวลา -->
        <div class="section-header" style="background: linear-gradient(90deg, #eff6ff 0%, #ffffff 100%); border-left: 5px solid #1e40af; color: #1e3a8a; margin-top: 24px;">
            🔬 การประเมินสรุปทางระบาดวิทยาและคอขวดเวลา (Epidemiological Cohort & Micro-Timeline Delay Assessment)
        </div>
        <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 16px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size: 13px; color: #64748b; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <span>การประเมินสถานะของเคสผู้ป่วยตามแบบจำลอง <b>Retrospective Cohort Study</b> และการตรวจจับจุดคอขวดเวลา (Bottlenecks)</span>
                <span style="font-size: 11px; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-weight: 700;">⚡ Real-time Auto Evaluation</span>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
                <!-- Card 1: Cohort Exposure Classification -->
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 14px; color: #1e3a8a;">
                            1. การจำแนกกลุ่มศึกษา (Cohort Classification)
                        </span>
                        <span style="font-size: 11px; background: #e2e8f0; color: #475569; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Kelsey et al. 1996</span>
                    </div>
                    <div id="cohort_badge_container" style="margin-bottom: 10px;"></div>
                    <div style="font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">
                        ปัจจัยสัมผัสคุกคามที่ตรวจพบ (Identified Exposure Determinants):
                    </div>
                    <div id="cohort_factors_container" style="flex: 1; font-size: 13px;"></div>
                </div>

                <!-- Card 2: Micro-Timeline Delay Assessment -->
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 14px; color: #1e3a8a;">
                            2. การประเมินคอขวดเวลา (Micro-Timeline Delay Assessment)
                        </span>
                        <span id="delay_count_badge" style="font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 700;"></span>
                    </div>
                    <div id="timeline_summary_badge" style="margin-bottom: 10px;"></div>
                    <div style="font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">
                        สถานะแต่ละช่วงเวลาส่งต่อ (Interval Benchmarks vs Actual):
                    </div>
                    <div id="timeline_delays_container" style="flex: 1; font-size: 12.5px;"></div>
                </div>
            </div>
        </div>

        <!-- Form 4 Completion Action Box -->
        <div style="margin-top: 25px; margin-bottom: 15px; padding: 20px; background: #ffffff; border: 1.5px solid #bae6fd; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); text-align: center;">
            <div style="font-size: 15px; font-weight: 700; color: #0369a1; margin-bottom: 6px;">
                ✓ สิ้นสุดการกรอกแบบบันทึกข้อมูล (Forms 1 – 4 ครบสมบูรณ์)
            </div>
            <p style="font-size: 13px; color: #64748b; margin-bottom: 14px;">
                กดปุ่มด้านล่างเพื่อบันทึกข้อมูลเคสเข้าสู่ระบบฐานข้อมูลอย่างปลอดภัย
            </p>
            <button type="button" class="btn btn-blue" onclick="finalizeCaseSave()" style="font-size: 15px; padding: 9px 28px; background: #0284c7; color: #ffffff; border-color: #0284c7; font-weight: 700; box-shadow: 0 2px 5px rgba(2, 132, 199, 0.3);">
                💾 บันทึกข้อมูลเคสนี้
            </button>
        </div>

    </div>
    """
