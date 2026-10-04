# -*- coding: utf-8 -*-
"""
Form 2 HTML Generator module
"""

def get_form2_html():
    return """
    <div id="page-form2" class="crf-page theme-form2">
        <!-- Header Box -->
        <div class="doc-header-box">
            <h2>แบบบันทึกข้อมูลการวิจัยทางคลินิก (CASE RECORD FORM: CRF)</h2>
            <h3>ส่วนที่ 2: เส้นเวลาส่งต่อ การปฏิบัติการขนส่งทางน้ำ และการบริบาลระหว่างทาง</h3>
            <p>Form 2: Amphibious Micro-Timeline, Ferry Operations & In-Transit Monitoring</p>
        </div>

        <!-- Lock Alert if Excluded -->
        <div id="f2_excluded_lock_alert" class="form-excluded-lock-banner" style="display: none; background: #fff1f2; border: 2px dashed #e11d48; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 4px;">⛔</div>
            <div style="font-size: 15.5px; font-weight: 800; color: #9f1239; margin-bottom: 4px;">
                ปิดกั้นการกรอกข้อมูล: ส่วนที่ 2 (Form 2) ถูกล็อก
            </div>
            <div style="font-size: 13px; color: #881337; line-height: 1.5;">
                เคสนี้ไม่ผ่านเกณฑ์การคัดกรอง (Excluded Case) ระบบจึงปิดกั้นการบันทึกข้อมูลเส้นเวลาส่งต่อ และการบริบาลระหว่างทาง<br>
                <span style="font-size: 12px; color: #64748b;">(หากต้องการแก้ไขความเข้าเกณฑ์ กรุณากลับไปปรับเปลี่ยนผลการตรวจสอบในส่วนที่ 1: Form 1)</span>
            </div>
        </div>

        <!-- Table 1: Identifiers -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">รหัสวิจัยผู้ป่วย (STUDY_ID)</td>
                <td style="width: 25%;">
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span>LANTA_</span>
                        <input type="text" id="f2_study_id" class="study-id-sync" placeholder="เช่น 001" style="font-weight: 700; color: #1e3a8a;">
                    </div>
                </td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เลขที่ใบส่งต่อ (Refer_ID)</td>
                <td style="width: 25%;">
                    <input type="text" id="f2_refer_id" class="refer-id-sync" placeholder="ระบุเลขที่ใบส่งต่อ">
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">เลขประจำตัวผู้ป่วย (HN / VN เกาะลันตา)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>HN:</span><input type="text" id="f2_hn" class="hn-sync" style="width: 80px;">
                        <span>VN:</span><input type="text" id="f2_vn" class="vn-sync" style="width: 80px;">
                    </div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">วันที่สกัดข้อมูล / ผู้สกัด (Abstractor)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f2_abs_date" class="date-sync" style="width: 125px;">
                        <span>ผู้สกัด:</span><input type="text" id="f2_abstractor" class="abs-sync" style="width: 100px;">
                    </div>
                </td>
            </tr>
        </table>

        <!-- Table 2: Ambulance Details -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">หมายเลขทะเบียนรถพยาบาล</td>
                <td style="width: 25%;"><input type="text" id="f2_amb_plate" placeholder="เช่น นข 1234 กระบี่"></td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">พยาบาลผู้ดูแล (Escort RN)</td>
                <td style="width: 25%;"><input type="text" id="f2_escort_rn" placeholder="ชื่อ-สกุล พยาบาล"></td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">พนักงานขับรถพยาบาล (Driver)</td>
                <td><input type="text" id="f2_driver" placeholder="ชื่อ-สกุล พนักงานขับรถ"></td>
                <td style="font-weight: 700; background: #f8fafc;">ประเภทรถพยาบาล</td>
                <td>
                    <label class="form-check" style="font-weight: 600;">
                        <input type="checkbox" id="f2_amb_type" checked> ALS Ambulance (รถกู้ชีพระดับสูง)
                    </label>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 1 -->
        <div class="section-header">หมวดที่ 1: บันทึกเส้นเวลาส่งต่อระดับไมโครความละเอียดสูง (T0 ถึง T4)</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 6%; text-align: center;">จุด</th>
                    <th style="width: 44%;">จุดสังเกตการณ์เชิงเวลา (Milestone Location)</th>
                    <th style="width: 32%;">วันและเวลาจริง (Date & Time: 24h)</th>
                    <th style="width: 18%;">แหล่งข้อมูลอ้างอิง</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T0</td>
                    <td>
                        <div>ผู้ป่วยเข้าสู่ห้องฉุกเฉิน รพ.เกาะลันตา (Island ED Arrival)</div>
                        <div style="font-size: 11.5px; color: #0284c7; font-weight: 600; margin-top: 2px;">🔗 ดึงข้อมูลอัตโนมัติจาก Form 1</div>
                    </td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t0_date" onchange="syncT0_fromF2(); calcForm2Timelines();" oninput="syncT0_fromF2(); calcForm2Timelines();" style="width: 125px; background: #f0fdf4; border-color: #86efac;">
                            <span>เวลา:</span><input type="time" id="f2_t0_time" onchange="syncT0_fromF2(); calcForm2Timelines();" oninput="syncT0_fromF2(); calcForm2Timelines();" style="background: #f0fdf4; border-color: #86efac;"><span>น.</span>
                        </div>
                    </td>
                    <td>EMR รพ.เกาะลันตา / สมุด ER</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T1</td>
                    <td>
                        <div>รถพยาบาลล้อหมุนออกจาก รพ.เกาะลันตา (ER Door-Out)</div>
                        <div style="font-size: 11.5px; color: #0284c7; font-weight: 600; margin-top: 2px;">🔗 ดึงข้อมูลอัตโนมัติจาก Form 1</div>
                    </td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t1_date" onchange="syncT1_fromF2(); calcForm2Timelines();" oninput="syncT1_fromF2(); calcForm2Timelines();" style="width: 125px; background: #f0fdf4; border-color: #86efac;">
                            <span>เวลา:</span><input type="time" id="f2_t1_time" onchange="syncT1_fromF2(); calcForm2Timelines();" oninput="syncT1_fromF2(); calcForm2Timelines();" style="background: #f0fdf4; border-color: #86efac;"><span>น.</span>
                        </div>
                    </td>
                    <td>EMS Run Sheet / GPS</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T2</td>
                    <td>รถพยาบาลถึงท่าเรือแพขนานยนต์คลองหมาก (Port Arrival)</td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t2_date" onchange="calcForm2Timelines();" style="width: 125px;">
                            <span>เวลา:</span><input type="time" id="f2_t2_time" onchange="calcForm2Timelines(); autoDetectFerryOperate();" oninput="calcForm2Timelines(); autoDetectFerryOperate();"><span>น.</span>
                        </div>
                    </td>
                    <td>บันทึกพยาบาล / GPS</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T3</td>
                    <td>ล้อรถเคลื่อนขึ้นบนแพขนานยนต์ (Embark Ro-Ro Ferry)</td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t3_embark_date" onchange="calcForm2Timelines();" style="width: 125px;">
                            <span>เวลา:</span><input type="time" id="f2_t3_embark_time" onchange="calcForm2Timelines();"><span>น.</span>
                        </div>
                    </td>
                    <td>บันทึกพยาบาล / GPS</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T3</td>
                    <td>ล้อรถแตะพื้นฝั่งแผ่นดินใหญ่ ท่าบ้านหัวหิน (Disembark Port)</td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t3_disembark_date" onchange="calcForm2Timelines();" style="width: 125px;">
                            <span>เวลา:</span><input type="time" id="f2_t3_disembark_time" onchange="calcForm2Timelines();"><span>น.</span>
                        </div>
                    </td>
                    <td>บันทึกพยาบาล / GPS</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T4</td>
                    <td>ผู้ป่วย ER รพ.กระบี่ (Krabi Hospital ER Door)</td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t4_date" onchange="syncT4(); calcForm2Timelines(); calcForm4Timelines();" style="width: 125px;">
                            <span>เวลา:</span><input type="time" id="f2_t4_time" onchange="syncT4(); calcForm2Timelines(); calcForm4Timelines();" oninput="syncT4(); calcForm2Timelines(); calcForm4Timelines();"><span>น.</span>
                        </div>
                    </td>
                    <td>EMR รพ.กระบี่ / GPS</td>
                </tr>
                <tr>
                    <td class="td-center" style="font-weight: 700; background: #eff6ff;">T5</td>
                    <td>
                        <div>ผู้ป่วยได้รับ Definitive Management (หัตถการ/การให้ยา/CT Scan)</div>
                        <div style="font-size: 11px; color: #2563eb; font-weight: 500;">(🔗 ลิ้งค์ข้อมูลอัตโนมัติกับ Form 4 หมวด 3: T5 การรักษาจำเพาะ)</div>
                    </td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span>วันที่:</span><input type="date" id="f2_t5_date" onchange="syncT5();" oninput="syncT5();" style="width: 125px;">
                            <span>เวลา:</span><input type="time" id="f2_t5_time" onchange="syncT5();" oninput="syncT5();"><span>น.</span>
                        </div>
                    </td>
                    <td>EMR รพ.กระบี่</td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 2 -->
        <div class="section-header">หมวดที่ 2: การคำนวณช่วงระยะเวลาและเปรียบเทียบเกณฑ์มาตรฐาน</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 25%;">ช่วงเวลา (Segment)</th>
                    <th style="width: 20%; text-align: center;">เวลาที่คำนวณได้</th>
                    <th style="width: 30%;">เกณฑ์มาตรฐาน (Benchmark)</th>
                    <th style="width: 25%;">ผลการประเมิน</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T0-1: Island DIDO</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t0_1_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>
                        &lt;= 45 นาที (Stroke/STEMI)<br>
                        &lt;= 60 นาที (Severe Trauma)
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_dido" id="f2_dido_ontime" value="ontime"> ทันเกณฑ์</label>
                            <label class="form-check"><input type="radio" name="f2_eval_dido" id="f2_dido_delay" value="delay"> ล่าช้า (&gt;45m/&gt;60m)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T2: Island Road</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t2_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>&lt;= 12 นาที (50–60 กม./ชม.)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_road" id="f2_road_ontime" value="ontime"> ทันเกณฑ์.</label>
                            <label class="form-check"><input type="radio" name="f2_eval_road" id="f2_road_delay" value="delay"> ล่าช้า (&gt;12 นาที)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T3: Water Crossing</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t3_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>&lt;= 24 นาที (ความเร็วเรือ 6–8 kn)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_water" id="f2_water_ontime" value="ontime"> ทันเกณฑ์ (&lt;=24m).</label>
                            <label class="form-check"><input type="radio" name="f2_eval_water" id="f2_water_delay" value="delay"> ล่าช้า (&gt;24m)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc; padding-left: 20px;">• เวลารอขึ้นแพ</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t_wait_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>&lt;= 5 นาที</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_wait" id="f2_wait_ontime" value="ontime"> ปกติ</label>
                            <label class="form-check"><input type="radio" name="f2_eval_wait" id="f2_wait_delay" value="delay"> รอคิวนาน</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T4: Mainland Highway</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t4_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>&lt;= 60 นาที (80–90 กม./ชม.)</td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_hwy" id="f2_hwy_ontime" value="ontime"> ทันเกณฑ์</label>
                            <label class="form-check"><input type="radio" name="f2_eval_hwy" id="f2_hwy_delay" value="delay"> ล่าช้า (&gt;60 นาที)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T_Total (System Time)</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t_total_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>
                        &lt;= 141 นาที (Stroke/ STEMI)<br>
                        &lt;= 156 นาที (Severe Trauma)
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_total" id="f2_total_ontime" value="ontime"> ทันเกณฑ์ (&lt;=141m/156m)</label>
                            <label class="form-check"><input type="radio" name="f2_eval_total" id="f2_total_delay" value="delay"> ล่าช้า (&gt;141m/156m)</label>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 700; background: #f8fafc;">T5 : Definitive Management</td>
                    <td class="td-center">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <input type="text" id="f2_t5_min" class="input-calc" style="width: 80px; text-align: center;" readonly placeholder="--">
                            <span>นาที</span>
                        </div>
                    </td>
                    <td>
                        &lt;= 156 นาที (Stroke)<br>
                        &lt;= 180 นาที (Severe Trauma/ STEMI)
                    </td>
                    <td>
                        <div class="check-group">
                            <label class="form-check"><input type="radio" name="f2_eval_t5" id="f2_t5_ontime" value="ontime"> ทันเกณฑ์ (&lt;=156m/180m)</label>
                            <label class="form-check"><input type="radio" name="f2_eval_t5" id="f2_t5_delay" value="delay"> ล่าช้า (&gt;156m/180m)</label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 3 -->
        <div class="section-header">หมวดที่ 3: การปฏิบัติการของแพขนานยนต์และท่าเทียบเรือ</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    ช่วงเวลาการเดินแพขนานยนต์ (FERRY_OPERATE)
                    <div style="font-size: 11px; color: #0284c7; font-weight: normal; margin-top: 2px;">(Auto คำนวณตามเวลา T2 ถึงท่าเรือ)</div>
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ferry_operate" id="f2_ferry_operate_0" value="0" onchange="syncFerryShiftFromF2();"> 0 = Scheduled Daytime (05:00–24:00 น.): บริการเดินเรือตามรอบปกติ</label>
                        <label class="form-check"><input type="radio" name="f2_ferry_operate" id="f2_ferry_operate_1" value="1" onchange="syncFerryShiftFromF2();"> 1 = Standby Off-Hour (24:00–05:00 น.): แพปิดบริการ ต้องโทรเรียกแพฉุกเฉิน (Emergency Call-out)</label>
                    </div>
                    <div id="f2_ferry_operate_badge" style="margin-top: 5px;"></div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">ความแออัดคิวรถหน้าท่าเรือ (PIER_CONGESTION)</td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_pier_congestion" value="0"> 0 = รถน้อย / สามารถนำรถพยาบาลขึ้นแพได้ทันที (Immediate Boarding)</label>
                        <label class="form-check"><input type="radio" name="f2_pier_congestion" value="1"> 1 = มีคิวรถติดสะสมหน้าท่าเรือคลองหมาก (Queue wait & congestion)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">จำนวนแพขนานยนต์ที่พร้อมให้บริการขณะนั้น</td>
                <td>
                    <div class="check-row">
                        <label class="form-check"><input type="radio" name="f2_ferry_count" value="1"> 1 ลำ</label>
                        <label class="form-check"><input type="radio" name="f2_ferry_count" value="2"> 2 ลำ</label>
                        <label class="form-check"><input type="radio" name="f2_ferry_count" value="3"> 3 ลำ</label>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 4 -->
        <div class="section-header">หมวดที่ 4: การติดตามสัญญาณชีพและการบริบาลต่อเนื่องระหว่างทาง</div>
        <table class="crf-table">
            <thead>
                <tr>
                    <th style="width: 25%;">จุดสังเกตการณ์ (Location)</th>
                    <th style="width: 10%; text-align: center;">เวลา (น.)</th>
                    <th style="width: 13%; text-align: center;">BP (mmHg)</th>
                    <th style="width: 9%; text-align: center;">HR (bpm)</th>
                    <th style="width: 8%; text-align: center;">RR (/min)</th>
                    <th style="width: 8%; text-align: center;">BT (°C)</th>
                    <th style="width: 8%; text-align: center;">O2Sat (%)</th>
                    <th style="width: 19%;">GCS / อาการ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 600;">1. ทางหลวงบนเกาะ (ก่อนลงแพ)</td>
                    <td><input type="time" id="f2_mon1_time"></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 2px;">
                            <input type="number" id="f2_mon1_sbp" style="width: 45px;" placeholder="SBP">/
                            <input type="number" id="f2_mon1_dbp" style="width: 45px;" placeholder="DBP">
                        </div>
                    </td>
                    <td><input type="number" id="f2_mon1_hr" style="width: 60px;"></td>
                    <td><input type="number" id="f2_mon1_rr" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon1_bt" step="0.1" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon1_spo2" style="width: 50px;"></td>
                    <td>
                        <div>GCS: <input type="number" id="f2_mon1_gcs" min="3" max="15" style="width: 60px; display: inline-block;"></div>
                        <div style="margin-top: 2px;">อาการ: <input type="text" id="f2_mon1_sym" style="width: 110px; display: inline-block;"></div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">2. บนแพขนานยนต์ (กลางน้ำ)</td>
                    <td><input type="time" id="f2_mon2_time"></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 2px;">
                            <input type="number" id="f2_mon2_sbp" style="width: 45px;" placeholder="SBP">/
                            <input type="number" id="f2_mon2_dbp" style="width: 45px;" placeholder="DBP">
                        </div>
                    </td>
                    <td><input type="number" id="f2_mon2_hr" style="width: 60px;"></td>
                    <td><input type="number" id="f2_mon2_rr" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon2_bt" step="0.1" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon2_spo2" style="width: 50px;"></td>
                    <td>
                        <div>GCS: <input type="number" id="f2_mon2_gcs" min="3" max="15" style="width: 60px; display: inline-block;"></div>
                        <div style="margin-top: 2px;">อาการ: <input type="text" id="f2_mon2_sym" style="width: 110px; display: inline-block;"></div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">3. ทางหลวงแผ่นดิน (กม. 35)</td>
                    <td><input type="time" id="f2_mon3_time"></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 2px;">
                            <input type="number" id="f2_mon3_sbp" style="width: 45px;" placeholder="SBP">/
                            <input type="number" id="f2_mon3_dbp" style="width: 45px;" placeholder="DBP">
                        </div>
                    </td>
                    <td><input type="number" id="f2_mon3_hr" style="width: 60px;"></td>
                    <td><input type="number" id="f2_mon3_rr" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon3_bt" step="0.1" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon3_spo2" style="width: 50px;"></td>
                    <td>
                        <div>GCS: <input type="number" id="f2_mon3_gcs" min="3" max="15" style="width: 60px; display: inline-block;"></div>
                        <div style="margin-top: 2px;">อาการ: <input type="text" id="f2_mon3_sym" style="width: 110px; display: inline-block;"></div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">4. หน้า ER รพ.กระบี่ (T4)</td>
                    <td><input type="time" id="f2_mon4_time"></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 2px;">
                            <input type="number" id="f2_mon4_sbp" style="width: 45px;" placeholder="SBP">/
                            <input type="number" id="f2_mon4_dbp" style="width: 45px;" placeholder="DBP">
                        </div>
                    </td>
                    <td><input type="number" id="f2_mon4_hr" style="width: 60px;"></td>
                    <td><input type="number" id="f2_mon4_rr" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon4_bt" step="0.1" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon4_spo2" style="width: 50px;"></td>
                    <td>
                        <div>GCS: <input type="number" id="f2_mon4_gcs" min="3" max="15" style="width: 60px; display: inline-block;"></div>
                        <div style="margin-top: 2px;">อาการ: <input type="text" id="f2_mon4_sym" style="width: 110px; display: inline-block;"></div>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">5. ER รพ.กระบี่ (T5)</td>
                    <td><input type="time" id="f2_mon5_time"></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 2px;">
                            <input type="number" id="f2_mon5_sbp" style="width: 45px;" placeholder="SBP">/
                            <input type="number" id="f2_mon5_dbp" style="width: 45px;" placeholder="DBP">
                        </div>
                    </td>
                    <td><input type="number" id="f2_mon5_hr" style="width: 60px;"></td>
                    <td><input type="number" id="f2_mon5_rr" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon5_bt" step="0.1" style="width: 50px;"></td>
                    <td><input type="number" id="f2_mon5_spo2" style="width: 50px;"></td>
                    <td>
                        <div>GCS: <input type="number" id="f2_mon5_gcs" min="3" max="15" style="width: 60px; display: inline-block;"></div>
                        <div style="margin-top: 2px;">อาการ: <input type="text" id="f2_mon5_sym" style="width: 110px; display: inline-block;"></div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- หมวดที่ 5 -->
        <div class="section-header">หมวดที่ 5: เหตุการณ์ไม่พึงประสงค์และการทรุดหนักระหว่างทาง</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    <div>1. ภาวะหัวใจหยุดเต้นระหว่างทาง</div>
                    <div style="font-size: 13px; color: #64748b;">(En-route CPR / Cardiac arrest)</div>
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ae_cpr" value="0" onchange="toggleCprDetails(); calcCompositeAE();"> 0 = ไม่มีภาวะหัวใจหยุดเต้นระหว่างทาง</label>
                        <label class="form-check"><input type="radio" name="f2_ae_cpr" value="1" onchange="toggleCprDetails(); calcCompositeAE();"> 1 = เกิดภาวะหัวใจหยุดเต้นและต้องทำ CPR ระหว่างทาง (En-route CPR)</label>
                    </div>
                    <div id="f2_cpr_details_box" style="margin-left: 20px; margin-top: 6px; opacity: 0.35; pointer-events: none;" class="check-group">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span>• ระยะเวลาทำ CPR รวม:</span>
                            <input type="number" id="f2_cpr_duration" style="width: 70px;" disabled>
                            <span>นาที</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px; margin-top: 4px;">
                            <span>• ผลลัพธ์:</span>
                            <label class="form-check"><input type="radio" name="f2_cpr_outcome" id="f2_cpr_outcome_rosc" value="rosc" disabled> ROSC ก่อนถึง ER</label>
                            <label class="form-check"><input type="radio" name="f2_cpr_outcome" id="f2_cpr_outcome_ongoing" value="ongoing" disabled> ทำ CPR ต่อเนื่องจนถึงห้องฉุกเฉิน รพ.ที่ใกล้ที่สุด</label>
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>2. การใส่ท่อช่วยหายใจฉุกเฉินระหว่างทาง</div>
                    <div style="font-size: 13px; color: #64748b;">(Emergency Intubation)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ae_intub" value="0" onchange="calcCompositeAE()"> 0 = ไม่ได้ใส่ระหว่างทาง</label>
                        <label class="form-check"><input type="radio" name="f2_ae_intub" value="1" onchange="calcCompositeAE()"> 1 = ต้องใส่ท่อช่วยหายใจฉุกเฉินระหว่างส่งต่อ (Emergency In-Transit Intubation)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>3. ภาวะช็อกและการเพิ่มยากระตุ้นความดัน</div>
                    <div style="font-size: 13px; color: #64748b;">(In-Transit Inotropes)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ae_inotropes" value="0" onchange="calcCompositeAE()"> 0 = ขนาดยาคงที่ / ไม่ต้องเริ่มยาใหม่</label>
                        <label class="form-check"><input type="radio" name="f2_ae_inotropes" value="1" onchange="calcCompositeAE()"> 1 = เกิดภาวะช็อก ต้องเริ่มยาใหม่ หรือปรับเพิ่มขนาดยากระตุ้นความดันฉุกเฉิน (Escalation &gt;= 50% จาก baseline เดิม)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>4. ท่อช่วยหายใจเลื่อนหลุด</div>
                    <div style="font-size: 13px; color: #64748b;">(ETT Dislodgement)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ae_dislodge" value="0" onchange="calcCompositeAE()"> 0 = ไม่มี</label>
                        <label class="form-check"><input type="radio" name="f2_ae_dislodge" value="1" onchange="calcCompositeAE()"> 1 = เกิดท่อช่วยหายใจเลื่อนหลุดระหว่างอยู่บนรถพยาบาล</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>5. เสียชีวิตระหว่างการส่งต่อ</div>
                    <div style="font-size: 13px; color: #64748b;">(In-Transit Death)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f2_ae_death" value="0" onchange="calcCompositeAE()"> 0 = รอดชีวิตจนถึง ER</label>
                        <label class="form-check"><input type="radio" name="f2_ae_death" value="1" onchange="calcCompositeAE()"> 1 = เสียชีวิตระหว่างทางบนรถพยาบาลหรือบนแพขนานยนต์</label>
                    </div>
                </td>
            </tr>
            <tr style="background: #f1f5f9;">
                <td style="font-weight: 700; color: #1e3a8a;">
                    <div>สรุปภาวะทรุดหนักระหว่างทางรวม</div>
                    <div style="font-size: 13px; font-weight: normal; color: #475569;">(Composite In-Transit Deterioration)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check" style="font-weight: 700; color: #166534;">
                            <input type="radio" name="f2_composite_ae" id="f2_comp_stable" value="0"> 0 = สัญญาณชีพคงที่ตลอดการเดินทาง (Stable)
                        </label>
                        <label class="form-check" style="font-weight: 700; color: #991b1b;">
                            <input type="radio" name="f2_composite_ae" id="f2_comp_event" value="1"> 1 = เกิดภาวะทรุดหนักวิกฤตระหว่างทาง (Critical Adverse Event)
                        </label>
                    </div>
                </td>
            </tr>
        </table>

    </div>
    """
