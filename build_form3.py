# -*- coding: utf-8 -*-
"""
Form 3 HTML Generator module
Form 3: Marine Hydro-Meteorological & Environmental Data (RTN / TMD)
"""

def get_form3_html():
    return """
    <div id="page-form3" class="crf-page theme-form3">
        <!-- Header Box -->
        <div class="doc-header-box">
            <h2>แบบบันทึกข้อมูลการวิจัยทางคลินิก (CASE RECORD FORM: CRF)</h2>
            <h3>ส่วนที่ 3: สภาพแวดล้อม อุทกศาสตร์ทางทะเล และอุตุนิยมวิทยา</h3>
            <p>Form 3: Marine Hydro-Meteorological & Environmental Data (RTN / TMD)</p>
        </div>

        <!-- Lock Alert if Excluded -->
        <div id="f3_excluded_lock_alert" class="form-excluded-lock-banner" style="display: none; background: #fff1f2; border: 2px dashed #e11d48; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 4px;">⛔</div>
            <div style="font-size: 15.5px; font-weight: 800; color: #9f1239; margin-bottom: 4px;">
                ปิดกั้นการกรอกข้อมูล: ส่วนที่ 3 (Form 3) ถูกล็อก
            </div>
            <div style="font-size: 13px; color: #881337; line-height: 1.5;">
                เคสนี้ไม่ผ่านเกณฑ์การคัดกรอง (Excluded Case) ระบบจึงปิดกั้นการบันทึกข้อมูลสภาพแวดล้อมและอุทก-อุตุนิยมวิทยา<br>
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
                        <input type="text" id="f3_study_id" class="study-id-sync" placeholder="เช่น 001" style="font-weight: 700; color: #1e3a8a;">
                    </div>
                </td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">เลขที่ใบส่งต่อ (Refer_ID)</td>
                <td style="width: 25%;">
                    <input type="text" id="f3_refer_id" class="refer-id-sync" placeholder="ระบุเลขที่ใบส่งต่อ">
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">เลขประจำตัวผู้ป่วย (HN / VN เกาะลันตา)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>HN:</span><input type="text" id="f3_hn" class="hn-sync" style="width: 80px;">
                        <span>VN:</span><input type="text" id="f3_vn" class="vn-sync" style="width: 80px;">
                    </div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">วันที่สกัดข้อมูล / ผู้สกัด (Abstractor)</td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <span>วันที่:</span><input type="date" id="f3_abs_date" class="date-sync" style="width: 125px;">
                        <span>ผู้สกัด:</span><input type="text" id="f3_abstractor" class="abs-sync" style="width: 100px;">
                    </div>
                </td>
            </tr>
        </table>

        <!-- Table 2: Marine Location Context -->
        <table class="crf-table">
            <tr>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">
                    <div>วันและเวลาข้ามฟาก</div>
                    <div>(T3)</div>
                </td>
                <td style="width: 25%;">
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <span>วันที่:</span><input type="date" id="f3_t3_date" onchange="calcForm3();" style="width: 125px;">
                        </div>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <span>เวลา:</span><input type="time" id="f3_t3_time" onchange="calcForm3();"><span>น.</span>
                        </div>
                    </div>
                </td>
                <td style="width: 25%; font-weight: 700; background: #f8fafc;">สถานีตรวจวัดอุทกศาสตร์</td>
                <td style="width: 25%;">
                    <div style="font-weight: 600;">สถานีเกาะลันตาใหญ่ (RTN)</div>
                    <div style="font-size: 13px; color: #475569;">ร่องน้ำคลองหมาก-หัวหิน (1.53 กม.) (0.83 NM)</div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">สถานีตรวจวัดสภาพอากาศ</td>
                <td>
                    <div style="font-weight: 600;">สถานีอุตุนิยมวิทยาเกาะลันตา / กระบี่ (TMD)</div>
                </td>
                <td style="font-weight: 700; background: #f8fafc;">พิกัดภูมิศาสตร์ร่องน้ำ</td>
                <td>
                    <div style="font-weight: 600; color: #0284c7;">Lat: 7.736° N, Long: 99.062° E</div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 1 -->
        <div class="section-header">หมวดที่ 1: ข้อมูลอุทกศาสตร์ทางทะเล กรมอุทกศาสตร์ กองทัพเรือ</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    <div>ระดับความสูงน้ำทะเลจริง ณ เวลาข้ามแพ</div>
                    <div style="font-size: 13px; color: #64748b;">(TIDE_HEIGHT_M)</div>
                </td>
                <td style="width: 65%;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span>ระดับน้ำจริง:</span>
                        <input type="number" id="f3_tide_height" step="0.01" style="width: 90px;" oninput="calcTide();" placeholder="เช่น 1.25">
                        <span>เมตร อ้างอิงระดับน้ำลงต่ำสุด (Astronomical tide level m LAT)</span>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>ภาวะน้ำลงต่ำสุดวิกฤต</div>
                    <div style="font-size: 13px; color: #64748b;">(TIDE_EXTREME_LOW)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check" style="font-weight: 600; color: #166534;">
                            <input type="radio" name="f3_tide_extreme" id="f3_tide_normal" value="0"> 0 = ระดับน้ำปกติ (&gt;= 1.0 เมตร LAT)
                        </label>
                        <label class="form-check" style="font-weight: 600; color: #991b1b;">
                            <input type="radio" name="f3_tide_extreme" id="f3_tide_low" value="1"> 1 = ภาวะน้ำลงต่ำสุดวิกฤต (&lt; 1.0 เมตร LAT)
                        </label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>ระยะการขึ้น-ลงของน้ำทะเล</div>
                    <div style="font-size: 13px; color: #64748b;">(TIDE_PHASE)</div>
                    <div style="font-size: 11px; color: #0284c7; font-weight: normal; margin-top: 2px;">(Auto เลือกตามระดับน้ำจริง TIDE_HEIGHT_M)</div>
                </td>
                <td>
                    <div class="check-row">
                        <label class="form-check"><input type="radio" name="f3_tide_phase" id="f3_tide_phase_flood" value="1" onchange="updateTidePhaseBadgeManual();"> 1 = น้ำขึ้น (Flood Tide)</label>
                        <label class="form-check"><input type="radio" name="f3_tide_phase" id="f3_tide_phase_ebb" value="2" onchange="updateTidePhaseBadgeManual();"> 2 = น้ำลง (Ebb Tide)</label>
                        <label class="form-check"><input type="radio" name="f3_tide_phase" id="f3_tide_phase_slack" value="3" onchange="updateTidePhaseBadgeManual();"> 3 = น้ำนิ่ง/น้ำทรง (Slack Water)</label>
                    </div>
                    <div id="f3_tide_phase_badge" style="margin-top: 4px;"></div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>ความเสี่ยงการติดสันดอนทรายในร่องน้ำ</div>
                    <div style="font-size: 13px; color: #64748b;">(Sandbar Grounding Risk)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_sandbar_risk" value="0"> 0 = ร่องน้ำลึกปกติ (No hazard: แพขนานยนต์แล่นตรงตามแนวร่องน้ำปกติ)</label>
                        <label class="form-check"><input type="radio" name="f3_sandbar_risk" value="1"> 1 = สันดอนทรายตื้นเขิน (High risk: แพต้องเดินเรืออ้อมแนวสันทราย ทำให้เสียเวลาเพิ่มขึ้น)</label>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 2 -->
        <div class="section-header">หมวดที่ 2: ข้อมูลอุตุนิยมวิทยาทางทะเลและสภาพอากาศ กรมอุตุนิยมวิทยา</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    <div>ฤดูกาลส่งต่อ</div>
                    <div style="font-size: 13px; color: #64748b;">(SEASON_MONSOON)</div>
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check" style="font-weight: 600;">
                            <input type="radio" name="f3_season" id="f3_season_monsoon" value="0"> 0 = Southwest Monsoon Season (ฤดูมรสุมตะวันตกเฉียงใต้: พฤษภาคม – ตุลาคม)
                        </label>
                        <label class="form-check" style="font-weight: 600;">
                            <input type="radio" name="f3_season" id="f3_season_dry" value="1"> 1 = Dry / High Season (ฤดูท่องเที่ยว / ฤดูแล้ง: พฤศจิกายน – เมษายน)
                        </label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>สภาพคลื่นลมทะเลอันดามัน</div>
                    <div style="font-size: 13px; color: #64748b;">(SEA_STATE)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_sea_state" value="0"> 0 = Calm (คลื่นสงบ &lt;= 1.0 เมตร)</label>
                        <label class="form-check"><input type="radio" name="f3_sea_state" value="1"> 1 = Moderate (คลื่นปานกลาง 1.0 – 2.0 เมตร)</label>
                        <label class="form-check"><input type="radio" name="f3_sea_state" value="2"> 2 = Rough (คลื่นลมแรงมรสุม &gt; 2.0 เมตร)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>สภาพฝนตกขณะส่งต่อ</div>
                    <div style="font-size: 13px; color: #64748b;">(Precipitation)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_precipitation" id="f3_precip_0" value="0" onchange="toggleRainDetails();"> 0 = Fair / No rain (อากาศแจ่มใส / ไม่มีฝน หรือฝนเล็กน้อย)</label>
                        <label class="form-check"><input type="radio" name="f3_precipitation" id="f3_precip_1" value="1" onchange="toggleRainDetails();"> 1 = Heavy rainfall / Storm (ฝนตกหนัก / พายุฝน)</label>
                    </div>
                </td>
            </tr>
            <tr id="row_f3_rainfall">
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>ปริมาณน้ำฝนสะสมรายชั่วโมง</div>
                    <div style="font-size: 13px; color: #64748b;">(Rain fall rate TMD)</div>
                    <div id="f3_rain_hint" style="font-size: 11px; font-weight: normal; margin-top: 2px;"></div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span>ปริมาณฝน:</span>
                        <input type="number" id="f3_rainfall_mm" step="0.1" style="width: 90px;" oninput="calcRain();" placeholder="เช่น 0.0">
                        <span>มม./ชม. (mm/hr)</span>
                    </div>
                </td>
            </tr>
            <tr id="row_f3_torrential">
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>เกณฑ์พายุฝนตกหนัก</div>
                    <div style="font-size: 13px; color: #64748b;">(Torrential Rain Rate: RAIN_MM_DAILY)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_torrential_rain" id="f3_rain_normal" value="0" onchange="scheduleAutoSave();"> 0 = ไม่เข้าเกณฑ์พายุฝนหนัก</label>
                        <label class="form-check"><input type="radio" name="f3_torrential_rain" id="f3_rain_heavy" value="1" onchange="scheduleAutoSave();"> 1 = พายุฝนตกหนักวิกฤต (&gt;= 10.0 มม./ชม. หรือ &gt;= 35.0 มม./วัน)</label>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 3 -->
        <div class="section-header">หมวดที่ 3: ปัจจัยปฏิทินและสิ่งแวดล้อมทางกาลเวลา</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc;">
                    <div>วันหยุดราชการ / เทศกาล</div>
                    <div style="font-size: 13px; color: #64748b;">(HOLIDAY)</div>
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_holiday" value="0"> 0 = วันธรรมดา (Weekday: วันจันทร์ – วันศุกร์)</label>
                        <label class="form-check"><input type="radio" name="f3_holiday" value="1"> 1 = วันหยุดยาวราชการ &gt;= 3 วัน (Official Public Long Holiday &gt;= 3 days)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>กะการเดินแพขนานยนต์</div>
                    <div style="font-size: 13px; color: #64748b;">(Ferry Operational Shift)</div>
                    <div style="font-size: 11px; color: #0284c7; font-weight: normal; margin-top: 2px;">(Auto เลือกตามเวลา T2 ถึงท่าเรือ)</div>
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="radio" name="f3_ferry_shift" id="f3_ferry_shift_0" value="0" onchange="syncFerryShiftFromF3();"> 0 = Scheduled Daytime (05:00–24:00 น.): บริการเดินเรือตามรอบปกติ</label>
                        <label class="form-check"><input type="radio" name="f3_ferry_shift" id="f3_ferry_shift_1" value="1" onchange="syncFerryShiftFromF3();"> 1 = Standby Off-Hour (24:00–05:00 น.): แพปิดบริการ ต้องโทรเรียกแพฉุกเฉิน (Emergency Call-out)</label>
                    </div>
                    <div id="f3_ferry_shift_badge" style="margin-top: 5px;"></div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc;">
                    <div>ช่วงเวรการทำงานห้องฉุกเฉินเกาะลันตา</div>
                    <div style="font-size: 13px; color: #64748b;">(ED Shift)</div>
                    <div style="font-size: 11px; color: #0284c7; font-weight: normal; margin-top: 2px;">(Auto เลือกตามเวลา T1 ออกจากห้องฉุกเฉิน)</div>
                </td>
                <td>
                    <div class="check-row">
                        <label class="form-check"><input type="radio" name="f3_ed_shift" id="f3_shift_morning" value="morning"> เวรเช้า (08:00–16:00 น.)</label>
                        <label class="form-check"><input type="radio" name="f3_ed_shift" id="f3_shift_afternoon" value="afternoon"> เวรบ่าย (16:00–24:00 น.)</label>
                        <label class="form-check"><input type="radio" name="f3_ed_shift" id="f3_shift_night" value="night"> เวรดึก (00:00–08:00 น.)</label>
                    </div>
                </td>
            </tr>
        </table>

        <!-- หมวดที่ 4 -->
        <div class="section-header">หมวดที่ 4: บันทึกการตรวจสอบแหล่งอ้างอิง</div>
        <table class="crf-table">
            <tr>
                <td style="width: 35%; font-weight: 700; background: #f8fafc; vertical-align: top;">
                    แหล่งข้อมูลอุทกศาสตร์ RTN
                </td>
                <td style="width: 65%;">
                    <div class="check-group">
                        <label class="form-check"><input type="checkbox" id="f3_ref_rtn_book"> ตารางมาตราน้ำ กรมอุทกศาสตร์ กองทัพเรือ เล่มประจำปี</label>
                        <label class="form-check"><input type="checkbox" id="f3_ref_rtn_portal"> ฐานข้อมูลดิจิทัลระบบทำนายน้ำ กรมอุทกศาสตร์ (RTN Portal)</label>
                        <div style="margin-top: 4px; display: flex; align-items: center; gap: 6px;">
                            <span>วันที่สืบค้นข้อมูล:</span>
                            <input type="date" id="f3_ref_rtn_date" style="width: 135px;">
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-weight: 700; background: #f8fafc; vertical-align: top;">
                    แหล่งข้อมูลอุตุนิยมวิทยา TMD
                </td>
                <td>
                    <div class="check-group">
                        <label class="form-check"><input type="checkbox" id="f3_ref_tmd_hourly"> รายงานตรวจอากาศประจำชั่วโมง สถานีอุตุนิยมวิทยาเกาะลันตา / สสจ.กระบี่</label>
                        <label class="form-check"><input type="checkbox" id="f3_ref_tmd_portal"> ฐานข้อมูลประวัติภูมิอากาศ กรมอุตุนิยมวิทยา (TMD Portal)</label>
                        <div style="margin-top: 4px; display: flex; align-items: center; gap: 6px;">
                            <span>วันที่สืบค้นข้อมูล:</span>
                            <input type="date" id="f3_ref_tmd_date" style="width: 135px;">
                        </div>
                    </div>
                </td>
            </tr>
        </table>

    </div>
    """
