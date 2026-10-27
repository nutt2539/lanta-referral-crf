# -*- coding: utf-8 -*-
"""
User Cases Dashboard HTML & CSS Generator
Provides a dedicated personal dashboard for logged-in accounts to view,
audit, and manage only the cases they have created/extracted.
"""

def get_user_dashboard_css():
    return """
        /* User Cases Dashboard Modal Styles */
        .user-dash-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .user-dash-stat-val {
            font-size: 24px;
            font-weight: 800;
            line-height: 1.1;
        }
        .user-dash-stat-label {
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
        }
        .user-dash-stat-sub {
            font-size: 11px;
            color: #94a3b8;
        }

        .user-dash-chart-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        .user-dash-table th {
            background: #f8fafc;
            color: #1e293b;
            font-weight: 700;
            padding: 9px 10px;
            border-bottom: 2px solid #cbd5e1;
            font-size: 12.5px;
        }
        .user-dash-table td {
            padding: 8px 10px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 12.5px;
            vertical-align: middle;
        }
        .user-dash-table tr:hover {
            background-color: #f8fafc;
        }
    """

def get_user_dashboard_html():
    return """
    <!-- User Personal Cases Dashboard Modal (My Cases) -->
    <div id="my-cases-dashboard-modal" class="modal-overlay" style="display: none; z-index: 2500;">
        <div class="modal-box" style="max-width: 1280px; width: 95%; max-height: 92vh; display: flex; flex-direction: column; border-radius: 10px; overflow: hidden; box-shadow: 0 16px 40px rgba(0,0,0,0.3); background: #f8fafc;">
            
            <!-- Modal Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #3b0764 0%, #581c87 100%); color: #ffffff; padding: 14px 22px; flex-shrink: 0; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 24px; line-height: 1;">📋</div>
                    <div>
                        <h3 style="font-size: 17px; font-weight: 800; color: #ffffff; margin: 0; display: flex; align-items: center; gap: 8px;">
                            <span>รายชื่อเคสที่ฉันสร้างไว้ (My Cases Dashboard)</span>
                            <span id="my-dash-count-badge" style="font-size: 11px; background: rgba(255,255,255,0.2); padding: 1px 8px; border-radius: 999px; font-weight: 700;">0 เคส</span>
                        </h3>
                        <p style="font-size: 12px; color: #e9d5ff; margin: 2px 0 0 0;">
                            ผู้บันทึก: <b id="my-dash-user-fullname">-</b> (<code id="my-dash-user-username" style="color: #ffffff; background: rgba(0,0,0,0.2); padding: 1px 5px; border-radius: 4px;">-</code>) • แสดงเฉพาะเคสที่คุณเป็นผู้บันทึกสกัดข้อมูล
                        </p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <button type="button" class="btn btn-success" onclick="closeMyCasesDashboard(); createNewCase();" style="font-size: 12.5px; padding: 5px 14px; font-weight: 700; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                        ➕ สร้างเคสใหม่
                    </button>
                    <button type="button" class="modal-close-btn" onclick="closeMyCasesDashboard()" style="color: #ffffff; font-size: 20px; padding: 2px 8px;" title="ปิดหน้าต่าง">✕</button>
                </div>
            </div>

            <!-- Modal Body (Scrollable) -->
            <div style="padding: 18px 22px; overflow-y: auto; flex: 1; display: flex; flex-direction: column; gap: 16px;">
                
                <!-- Section 1: Overview Summary Stat Cards -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                    <div class="user-dash-card" style="border-left: 4px solid #7c3aed;">
                        <div class="user-dash-stat-label">เคสทั้งหมดที่ฉันบันทึก</div>
                        <div class="user-dash-stat-val" id="my-stat-total-cases" style="color: #581c87;">0</div>
                        <div class="user-dash-stat-sub" id="my-stat-total-sub">บันทึกอยู่ในเบราว์เซอร์นี้</div>
                    </div>
                    <div class="user-dash-card" style="border-left: 4px solid #16a34a;">
                        <div class="user-dash-stat-label">บันทึกข้อมูลครบถ้วน 100%</div>
                        <div class="user-dash-stat-val" id="my-stat-completed-cases" style="color: #15803d;">0</div>
                        <div class="user-dash-stat-sub" id="my-stat-completed-sub">0% ของเคสทั้งหมด</div>
                    </div>
                    <div class="user-dash-card" style="border-left: 4px solid #f59e0b;">
                        <div class="user-dash-stat-label">ยังไม่สมบูรณ์ (ต้องเติมช่องว่าง)</div>
                        <div class="user-dash-stat-val" id="my-stat-pending-cases" style="color: #b45309;">0</div>
                        <div class="user-dash-stat-sub" id="my-stat-pending-sub">มีจุดที่ยังไม่ได้ระบุ</div>
                    </div>
                    <div class="user-dash-card" style="border-left: 4px solid #2563eb;">
                        <div class="user-dash-stat-label">ความสมบูรณ์ของฟอร์มเฉลี่ย</div>
                        <div class="user-dash-stat-val" id="my-stat-avg-completeness" style="color: #1d4ed8;">100%</div>
                        <div class="user-dash-stat-sub" id="my-stat-avg-sub">คำนวณจากทุกส่วน Form 1–4</div>
                    </div>
                </div>

                <!-- Section 2: Visual Charts & Form Progress Breakdown -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px;">
                    <!-- Chart 1: Disease Distribution -->
                    <div class="user-dash-chart-card">
                        <div style="font-weight: 700; font-size: 13.5px; color: #1e293b; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                            <span>🩺 สัดส่วนกลุ่มโรคที่ฉันบันทึก</span>
                            <span style="font-size: 11px; color: #64748b; font-weight: normal;">(Target Conditions)</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div style="position: relative; width: 100px; height: 100px; flex-shrink: 0;">
                                <div id="my-pie-chart-disease" style="width: 100%; height: 100%; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center;">
                                    <div style="width: 58px; height: 58px; border-radius: 50%; background: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
                                        <span id="my-pie-center-disease" style="font-size: 16px; font-weight: 800; color: #1e293b;">0</span>
                                        <span style="font-size: 9.5px; color: #64748b;">เคส</span>
                                    </div>
                                </div>
                            </div>
                            <div id="my-pie-legend-disease" style="flex: 1; font-size: 11.5px; display: flex; flex-direction: column; gap: 5px;">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>

                    <!-- Chart 2: Completeness Progress Status -->
                    <div class="user-dash-chart-card">
                        <div style="font-weight: 700; font-size: 13.5px; color: #1e293b; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                            <span>📊 ความคืบหน้าการกรอกข้อมูล</span>
                            <span style="font-size: 11px; color: #64748b; font-weight: normal;">(Completeness Tier)</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div style="position: relative; width: 100px; height: 100px; flex-shrink: 0;">
                                <div id="my-pie-chart-comp" style="width: 100%; height: 100%; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center;">
                                    <div style="width: 58px; height: 58px; border-radius: 50%; background: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
                                        <span id="my-pie-center-comp" style="font-size: 15px; font-weight: 800; color: #15803d;">100%</span>
                                        <span style="font-size: 9.5px; color: #64748b;">เฉลี่ย</span>
                                    </div>
                                </div>
                            </div>
                            <div id="my-pie-legend-comp" style="flex: 1; font-size: 11.5px; display: flex; flex-direction: column; gap: 5px;">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>

                    <!-- Chart 3: Progress by Form (Form 1 to 4) -->
                    <div class="user-dash-chart-card">
                        <div style="font-weight: 700; font-size: 13.5px; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                            <span>📑 ความครบถ้วนเฉลี่ยแบ่งตามแบบบันทึก (Form 1–4)</span>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 7px; margin-top: 6px;">
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #334155; margin-bottom: 2px;">
                                    <span>Form 1: คัดกรอง & รพ.เกาะลันตา</span>
                                    <span id="my-form1-pct-label">100%</span>
                                </div>
                                <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                    <div id="my-form1-bar" style="width: 100%; background: #1e40af; height: 100%; transition: width 0.3s ease;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #334155; margin-bottom: 2px;">
                                    <span>Form 2: การเดินทางส่งต่อ (EMS)</span>
                                    <span id="my-form2-pct-label">100%</span>
                                </div>
                                <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                    <div id="my-form2-bar" style="width: 100%; background: #0f766e; height: 100%; transition: width 0.3s ease;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #334155; margin-bottom: 2px;">
                                    <span>Form 3: ปัจจัยกำหนดความล่าช้า</span>
                                    <span id="my-form3-pct-label">100%</span>
                                </div>
                                <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                    <div id="my-form3-bar" style="width: 100%; background: #7e22ce; height: 100%; transition: width 0.3s ease;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #334155; margin-bottom: 2px;">
                                    <span>Form 4: ผลลัพธ์แรกรับ รพ.กระบี่</span>
                                    <span id="my-form4-pct-label">100%</span>
                                </div>
                                <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                    <div id="my-form4-bar" style="width: 100%; background: #b91c1c; height: 100%; transition: width 0.3s ease;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Section 3: Filter & Search Bar -->
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div style="display: flex; gap: 8px; align-items: center; flex: 1; min-width: 280px;">
                        <input type="text" id="my-cases-search" placeholder="🔍 ค้นหารหัสเคส (Study ID), HN, เลขที่ Refer หรือชื่อผู้ป่วย..."
                               style="width: 100%; max-width: 380px; padding: 6px 12px; font-size: 13px; border: 1.5px solid #cbd5e1; border-radius: 6px;"
                               oninput="renderMyCasesDashboard()">
                        <select id="my-cases-filter-disease" onchange="renderMyCasesDashboard()" style="padding: 6px 10px; font-size: 13px; border: 1.5px solid #cbd5e1; border-radius: 6px;">
                            <option value="">-- กลุ่มโรคทั้งหมด --</option>
                            <option value="stemi">STEMI / ACS</option>
                            <option value="ais">Acute Stroke</option>
                            <option value="trauma">Severe Trauma</option>
                        </select>
                        <select id="my-cases-filter-status" onchange="renderMyCasesDashboard()" style="padding: 6px 10px; font-size: 13px; border: 1.5px solid #cbd5e1; border-radius: 6px;">
                            <option value="">-- ความสมบูรณ์ทั้งหมด --</option>
                            <option value="complete">✓ บันทึกครบ 100%</option>
                            <option value="incomplete">⚠️ ยังไม่สมบูรณ์ (มีช่องว่าง)</option>
                        </select>
                    </div>
                    <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">
                        แสดง <span id="my-cases-table-count" style="color: #581c87; font-weight: 800;">0</span> เคส
                    </div>
                </div>

                <!-- Section 4: Main Cases Table -->
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <div style="overflow-x: auto;">
                        <table class="user-dash-table" style="width: 100%; border-collapse: collapse; min-width: 980px;">
                            <thead>
                                <tr>
                                    <th style="width: 8%; text-align: center;">ลำดับ / รหัส</th>
                                    <th style="width: 15%; text-align: center;">วันที่สร้าง+เวลา</th>
                                    <th style="width: 12%;">HN</th>
                                    <th style="width: 18%;">ชื่อ-นามสกุลผู้ป่วย</th>
                                    <th style="width: 12%; text-align: center;">วันที่ refer</th>
                                    <th style="width: 12%; text-align: center;">กลุ่มโรค</th>
                                    <th style="width: 14%; text-align: center;">% ความคืบหน้าของ form</th>
                                    <th style="width: 9%; text-align: center;">การจัดการ</th>
                                </tr>
                            </thead>
                            <tbody id="my-cases-tbody">
                                <!-- Populated dynamically by renderMyCasesDashboard() -->
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>

            <!-- Modal Footer -->
            <div style="background: #f1f5f9; border-top: 1px solid #e2e8f0; padding: 10px 22px; display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;">
                <div style="font-size: 12px; color: #64748b;">
                    💡 <i>คำแนะนำ: คลิกที่แถบ % ความคืบหน้า หรือกดปุ่ม "📝 เติมช่องว่าง" เพื่อไปยังจุดที่ยังไม่ได้ระบุข้อมูลได้ทันที</i>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button type="button" class="btn btn-outline" onclick="closeMyCasesDashboard()" style="padding: 5px 16px; font-size: 13px;">
                        ปิดหน้าต่าง
                    </button>
                </div>
            </div>

        </div>
    </div>
    """
