# -*- coding: utf-8 -*-
"""
Admin Dashboard HTML & CSS Generator
Implements complete Clinical Research Objectives Dashboards:
- Primary Objective: Definitive Treatment Benchmarks (Door-to-Balloon, Needle, OR)
- Secondary Objective 01: Micro-timeline Intervals (T1-5) & Benchmark Breaches
- Secondary Objective 02: Bottlenecks & Delay Triggers (Patient, Operational, Maritime-Environmental)
- Secondary Objective 03: Clinical Deterioration & Cohort Comparison (Relative Risk, 2x2 Tables)
- Overview & Case Directory
"""

def get_admin_dashboard_css():
    return """
        /* Admin Dashboard Sub-Tabs & Research Visuals */
        .admin-tab-nav {
            display: flex;
            gap: 4px;
            padding: 8px 18px 0 18px;
            background: #ffffff;
            border-bottom: 2px solid #e2e8f0;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        .admin-tab-btn {
            padding: 8px 14px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            font-size: 13px;
            font-weight: 600;
            color: #64748b;
            cursor: pointer;
            white-space: nowrap;
            border-radius: 6px 6px 0 0;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .admin-tab-btn:hover {
            color: #1e40af;
            background: #f8fafc;
        }
        .admin-tab-btn.active {
            color: #1e40af;
            border-bottom-color: #1e40af;
            background: #eff6ff;
            font-weight: 700;
        }
        .admin-tab-pane {
            animation: modalFadeIn 0.2s ease-out;
        }
        .research-banner {
            border-radius: 8px;
            padding: 12px 18px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .research-card {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .research-kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }
        .research-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
        }
        .research-table th {
            background: #f1f5f9;
            color: #1e293b;
            font-weight: 700;
            padding: 8px 10px;
            border: 1px solid #cbd5e1;
            text-align: center;
        }
        .research-table td {
            padding: 8px 10px;
            border: 1px solid #e2e8f0;
            color: #334155;
        }
        .research-table tr:nth-child(even) {
            background: #f8fafc;
        }
        .bar-horizontal-track {
            background: #f1f5f9;
            border-radius: 999px;
            height: 10px;
            overflow: hidden;
            width: 100%;
            position: relative;
        }
        .bar-horizontal-fill {
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }
    """

def get_admin_dashboard_html():
    return """
    <!-- Admin Dashboard Modal -->
    <div id="admin-dashboard-modal" class="modal-overlay" style="display:none;">
        <div class="modal-box modal-box-large">
            <!-- Dashboard Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e1b4b 0%, #3b0764 100%); color: #ffffff; padding: 12px 20px; border-radius: 8px 8px 0 0;">
                <div>
                    <h2 style="font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px; color: #ffffff;">
                        <span>📊 แดชบอร์ดสรุปและวิเคราะห์ผลการวิจัย (Research Admin Dashboard)</span>
                        <span style="font-size: 11px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 999px; font-weight: 500;">MSc Thesis</span>
                    </h2>
                    <p style="font-size: 12.5px; opacity: 0.85; margin-top: 1px; color: #e2e8f0;">
                        ระบบสารสนเทศและการวิเคราะห์ข้อมูลผู้ป่วยส่งต่อฉุกเฉิน เกาะลันตา ➔ รพ.กระบี่ ตามกรอบวัตถุประสงค์วิจัย
                    </p>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <button type="button" class="btn btn-success" onclick="exportToExcel()" style="font-size: 13px; padding: 4px 10px;" title="ดาวน์โหลดฐานข้อมูลทุกเคสเป็นไฟล์ Excel (.xlsx)">
                        📥 Export Excel
                    </button>
                    <button type="button" class="btn btn-blue" onclick="openPdfModal()" style="font-size: 13px; padding: 4px 10px;" title="ส่งออกรายงานข้อมูลคนไข้เป็น PDF หรือสั่งพิมพ์">
                        📄 Export PDF
                    </button>
                    <button type="button" class="btn btn-outline" onclick="adminLogout()" style="font-size: 13px; padding: 4px 10px; color: #fca5a5; border-color: rgba(255,255,255,0.3); background: transparent;" title="ออกจากระบบผู้ดูแล">
                        🔒 ล็อคระบบ
                    </button>
                    <button type="button" class="modal-close-btn" onclick="closeAdminDashboard()" style="color: #ffffff; font-size: 18px;" title="ปิดหน้าต่าง">✕</button>
                </div>
            </div>

            <!-- Admin Sub-Tabs Navigation (ตาม Research Objectives) -->
            <div class="admin-tab-nav">
                <button type="button" class="admin-tab-btn active" id="admin-tab-btn-overview" onclick="switchAdminSubTab('overview')">
                    <span>📋 ภาพรวม & รายชื่อเคส</span>
                </button>
                <button type="button" class="admin-tab-btn" id="admin-tab-btn-primary" onclick="switchAdminSubTab('primary')">
                    <span>🏆 Primary: Definitive Benchmarks</span>
                </button>
                <button type="button" class="admin-tab-btn" id="admin-tab-btn-sec1" onclick="switchAdminSubTab('sec1')">
                    <span>⏱️ Sec 01: Micro-timelines</span>
                </button>
                <button type="button" class="admin-tab-btn" id="admin-tab-btn-sec2" onclick="switchAdminSubTab('sec2')">
                    <span>🔍 Sec 02: Bottlenecks & Triggers</span>
                </button>
                <button type="button" class="admin-tab-btn" id="admin-tab-btn-sec3" onclick="switchAdminSubTab('sec3')">
                    <span>📉 Sec 03: Clinical Outcomes & RR</span>
                </button>
            </div>

            <!-- Global Cohort Filter Toolbar (มีผลต่อการวิเคราะห์ทุกแท็บ) -->
            <div style="background: #ffffff; border-bottom: 1px solid #cbd5e1; padding: 8px 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;">
                <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; font-size: 13px;">
                    <span style="font-weight: 700; color: #1e3a8a; display: flex; align-items: center; gap: 5px;">
                        <span>🎯 ตัวกรอง Cohort:</span>
                    </span>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <span style="font-weight: 600; color: #475569;">กลุ่มโรค:</span>
                        <select id="admin-filter-disease" onchange="renderAdminDashboard()" style="padding: 3px 8px; font-size: 12.5px; border: 1px solid #cbd5e1; border-radius: 4px; background: #ffffff;">
                            <option value="">ทั้งหมด (All Diseases)</option>
                            <option value="stemi">STEMI / ACS</option>
                            <option value="ais">Stroke (AIS)</option>
                            <option value="trauma">Severe Trauma</option>
                        </select>
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <span style="font-weight: 600; color: #475569;">Triage ESI:</span>
                        <select id="admin-filter-esi" onchange="renderAdminDashboard()" style="padding: 3px 8px; font-size: 12.5px; border: 1px solid #cbd5e1; border-radius: 4px; background: #ffffff;">
                            <option value="">ทุกระดับ (All ESI)</option>
                            <option value="1">ESI 1 (Resuscitation)</option>
                            <option value="2">ESI 2 (Emergent)</option>
                            <option value="3">ESI 3 (Urgent)</option>
                            <option value="4">ESI 4 (Semi-urgent)</option>
                            <option value="5">ESI 5 (Non-urgent)</option>
                        </select>
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <span style="font-weight: 600; color: #475569;">สถานะ Cohort:</span>
                        <select id="admin-filter-cohort" onchange="renderAdminDashboard()" style="padding: 3px 8px; font-size: 12.5px; border: 1px solid #cbd5e1; border-radius: 4px; background: #ffffff;">
                            <option value="">ทั้งหมด (All Cases)</option>
                            <option value="exposed">กลุ่ม Exposed (Delay / Triggers)</option>
                            <option value="unexposed">กลุ่ม Unexposed / Control (On-time)</option>
                        </select>
                    </div>
                    <button type="button" class="btn btn-outline" onclick="resetAdminFilters()" style="padding: 2px 8px; font-size: 12px;" title="รีเซ็ตตัวกรองทั้งหมด">
                        🔄 รีเซ็ต
                    </button>
                </div>
                <div style="font-size: 12.5px; color: #475569; font-weight: 500;">
                    กำลังวิเคราะห์: <b id="admin-filter-count-badge" style="color: #1e40af; font-size: 14px;">0</b> จากทั้งหมด <b id="admin-total-cases-badge" style="color: #0f172a;">0</b> เคส
                </div>
            </div>

            <!-- Modal Scrollable Content -->
            <div style="padding: 16px 20px; background: #f8fafc; max-height: calc(85vh - 145px); overflow-y: auto;">

                <!-- ========================================== -->
                <!-- TAB 1: OVERVIEW & CASE DIRECTORY           -->
                <!-- ========================================== -->
                <div id="admin-tab-content-overview" class="admin-tab-pane">
                    <!-- Summary Stat Cards -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #1e40af; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">ผู้ป่วยใน Cohort ทั้งหมด</div>
                            <div id="stat-total-patients" style="font-size: 26px; font-weight: 700; color: #1e40af; line-height: 1.2; margin-top: 2px;">0</div>
                            <div style="font-size: 11.5px; color: #94a3b8;">เคสที่บันทึกแล้วในเบราว์เซอร์</div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #0f766e; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">เวลาส่งต่อเฉลี่ย (T0 ➔ T5)</div>
                            <div id="stat-mean-time" style="font-size: 26px; font-weight: 700; color: #0f766e; line-height: 1.2; margin-top: 2px;">0 <span style="font-size: 14px; font-weight: 500;">นาที</span></div>
                            <div id="stat-time-detail" style="font-size: 11.5px; color: #94a3b8;">จากเคสที่มีข้อมูลเวลาครบ</div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #b91c1c; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">ผู้ป่วยวิกฤตฉุกเฉิน (ESI 1)</div>
                            <div id="stat-esi1-count" style="font-size: 26px; font-weight: 700; color: #b91c1c; line-height: 1.2; margin-top: 2px;">0</div>
                            <div id="stat-esi1-pct" style="font-size: 11.5px; color: #94a3b8;">0% ของผู้ป่วยทั้งหมด</div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #16a34a; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">อัตรารอดชีวิต 24 ชม. รพ.กระบี่</div>
                            <div id="stat-survival-rate" style="font-size: 26px; font-weight: 700; color: #16a34a; line-height: 1.2; margin-top: 2px;">100%</div>
                            <div id="stat-survival-detail" style="font-size: 11.5px; color: #94a3b8;">Early Survival Outcome</div>
                        </div>
                    </div>

                    <!-- Clinical Research Pie Charts Overview -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                            <div style="font-size: 14px; font-weight: 700; color: #1e3a8a; display: flex; align-items: center; gap: 6px;">
                                <span>📊 แผนภูมิวิเคราะห์สัดส่วนข้อมูลทางคลินิก (Clinical Research Distribution)</span>
                            </div>
                            <span style="font-size: 11.5px; color: #64748b; font-weight: 500;">สรุปสัดส่วนตัวแปรสำคัญจากฐานข้อมูลจริง</span>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                                <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">🫀 กลุ่มโรคเป้าหมาย (Disease)</div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div id="pie-chart-disease" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                        <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                            <span id="pie-center-disease" style="font-size: 13px; font-weight: 700; color: #1e293b; line-height: 1;">0</span>
                                            <span style="font-size: 8.5px; color: #64748b;">เคส</span>
                                        </div>
                                    </div>
                                    <div id="pie-legend-disease" style="flex: 1; min-width: 0;"></div>
                                </div>
                            </div>

                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                                <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">⏱️ ความทันเวลาส่งต่อ (≤ 3 ชม.)</div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div id="pie-chart-timeliness" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                        <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                            <span id="pie-center-timeliness" style="font-size: 13px; font-weight: 700; color: #059669; line-height: 1;">0%</span>
                                            <span style="font-size: 8.5px; color: #64748b;">ทันเวลา</span>
                                        </div>
                                    </div>
                                    <div id="pie-legend-timeliness" style="flex: 1; min-width: 0;"></div>
                                </div>
                            </div>

                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                                <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">🏥 ผลลัพธ์รอดชีวิต 24 ชม.</div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div id="pie-chart-survival" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                        <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                            <span id="pie-center-survival" style="font-size: 13px; font-weight: 700; color: #16a34a; line-height: 1;">0%</span>
                                            <span style="font-size: 8.5px; color: #64748b;">รอดชีวิต</span>
                                        </div>
                                    </div>
                                    <div id="pie-legend-survival" style="flex: 1; min-width: 0;"></div>
                                </div>
                            </div>

                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                                <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">🚨 ระดับความเร่งด่วน (ESI)</div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div id="pie-chart-esi" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                        <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                            <span id="pie-center-esi" style="font-size: 13px; font-weight: 700; color: #1e293b; line-height: 1;">0</span>
                                            <span style="font-size: 8.5px; color: #64748b;">เคส</span>
                                        </div>
                                    </div>
                                    <div id="pie-legend-esi" style="flex: 1; min-width: 0;"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Search & Case Directory Controls -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
                        <div style="display: flex; gap: 8px; align-items: center; flex: 1; min-width: 260px;">
                            <span style="font-weight: 600; font-size: 13.5px;">🔍 ค้นหาเคส:</span>
                            <input type="text" id="admin-search-box" oninput="renderAdminDashboard()" placeholder="พิมพ์ค้นหา STUDY_ID, HN, หรือเลขใบ Refer..." style="padding: 4px 8px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 4px; flex: 1;">
                        </div>
                        <div>
                            <button type="button" class="btn btn-primary" onclick="createNewCase(); closeAdminDashboard();" style="font-size: 13px; padding: 5px 12px;">
                                ➕ สร้างเคสใหม่
                            </button>
                        </div>
                    </div>

                    <!-- Patient Cases Table -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div class="table-responsive" style="margin-bottom: 0;">
                            <table class="crf-table" style="margin-bottom: 0; font-size: 13px; width: 100%;">
                                <thead>
                                    <tr style="background: #f1f5f9;">
                                        <th style="width: 100px; text-align: center;">STUDY_ID</th>
                                        <th style="width: 130px;">HN / Refer_ID</th>
                                        <th style="width: 100px; text-align: center;">อายุ / เพศ</th>
                                        <th style="width: 90px; text-align: center;">Triage ESI</th>
                                        <th>หมวดโรค / การวินิจฉัย</th>
                                        <th style="width: 130px; text-align: center;">เวลาส่งต่อรวม</th>
                                        <th style="width: 90px; text-align: center;">RTS (เกาะ/กระบี่)</th>
                                        <th style="width: 100px; text-align: center;">ผลลัพธ์ 24 ชม.</th>
                                        <th style="width: 200px; text-align: center;">จัดการข้อมูล</th>
                                    </tr>
                                </thead>
                                <tbody id="admin-cases-tbody">
                                    <!-- Populated dynamically by JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ========================================== -->
                <!-- TAB 2: PRIMARY OBJECTIVE                   -->
                <!-- ========================================== -->
                <div id="admin-tab-content-primary" class="admin-tab-pane" style="display:none;">
                    <div class="research-banner" style="background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); border: 1px solid #c7d2fe; border-left: 5px solid #4338ca;">
                        <div>
                            <div style="font-size: 11.5px; font-weight: 800; color: #4338ca; letter-spacing: 0.5px; text-transform: uppercase;">
                                🏆 PRIMARY OBJECTIVE • "Timeliness"
                            </div>
                            <div style="font-size: 16px; font-weight: 700; color: #1e1b4b; margin-top: 2px;">
                                Incidence of Achieving Definitive Treatment Benchmarks
                            </div>
                            <div style="font-size: 12.5px; color: #4338ca; opacity: 0.85; margin-top: 2px;">
                                To determine the incidence of achieving definitive treatment benchmarks (Door-to-Balloon, Needle, OR) in an inception cohort of island emergency patients transferred to a mainland referral hospital.
                            </div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #c7d2fe; border-radius: 8px; padding: 8px 16px; text-align: right; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <div style="font-size: 11.5px; color: #64748b; font-weight: 600;">อัตราการบรรลุเกณฑ์รวม (Overall)</div>
                            <div id="prim-overall-rate" style="font-size: 26px; font-weight: 800; color: #16a34a; line-height: 1.1;">0%</div>
                            <div id="prim-overall-detail" style="font-size: 11px; color: #94a3b8;">0 / 0 เคสที่ได้รับการรักษา</div>
                        </div>
                    </div>

                    <!-- Top 4 KPI Cards for Definitive Treatment -->
                    <div class="research-kpi-grid">
                        <!-- Card 1: All Combined -->
                        <div class="research-card" style="border-left: 4px solid #16a34a;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">ทุกหัตถการรวม (Combined Benchmark)</div>
                            <div id="prim-card-combined-pct" style="font-size: 24px; font-weight: 700; color: #16a34a; margin-top: 2px;">0%</div>
                            <div id="prim-card-combined-sub" style="font-size: 11.5px; color: #94a3b8;">บรรลุ 0 จาก 0 เคส</div>
                        </div>
                        <!-- Card 2: STEMI PCI -->
                        <div class="research-card" style="border-left: 4px solid #dc2626;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">STEMI: Door-to-Balloon (≤ 180 น.)</div>
                            <div id="prim-card-stemi-pct" style="font-size: 24px; font-weight: 700; color: #dc2626; margin-top: 2px;">0%</div>
                            <div id="prim-card-stemi-mean" style="font-size: 11.5px; color: #475569;">เวลาเฉลี่ย: -- นาที</div>
                        </div>
                        <!-- Card 3: Stroke IV rtPA -->
                        <div class="research-card" style="border-left: 4px solid #d97706;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">Stroke: Onset-to-Needle (≤ 4.5 ชม.)</div>
                            <div id="prim-card-stroke-pct" style="font-size: 24px; font-weight: 700; color: #d97706; margin-top: 2px;">0%</div>
                            <div id="prim-card-stroke-mean" style="font-size: 11.5px; color: #475569;">เวลาเฉลี่ย: -- นาที</div>
                        </div>
                        <!-- Card 4: Severe Trauma OR/CT -->
                        <div class="research-card" style="border-left: 4px solid #7c3aed;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">Trauma: Emergent OR / CT</div>
                            <div id="prim-card-trauma-pct" style="font-size: 24px; font-weight: 700; color: #7c3aed; margin-top: 2px;">0%</div>
                            <div id="prim-card-trauma-mean" style="font-size: 11.5px; color: #475569;">OR: -- น. | CT: -- น.</div>
                        </div>
                    </div>

                    <!-- Charts Grid: Benchmark Achievement & Time to Intervention -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 14px; margin-bottom: 16px;">
                        <!-- Chart 1: Incidence Achievement Bar Chart -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>📊 สัดส่วนการบรรลุเกณฑ์เวลาจำเพาะ (Benchmark Achievement Rate)</span>
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                                เปรียบเทียบสัดส่วน บรรลุเกณฑ์ (Achieved) vs หลุดเกณฑ์ (Missed) แยกรายกลุ่มโรค
                            </div>
                            <div id="prim-chart-bars" style="display: flex; flex-direction: column; gap: 12px;">
                                <!-- Rendered dynamically by JS -->
                            </div>
                        </div>

                        <!-- Chart 2: Mean Duration vs Target Benchmark -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>⏱️ เวลาเฉลี่ยจนถึงหัตถการจริง vs กรอบเวลาเป้าหมาย (Golden Window)</span>
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                                เปรียบเทียบระยะเวลาจริงเฉลี่ย (Mean Duration) กับเส้นเกณฑ์มาตรฐานสากล
                            </div>
                            <div id="prim-chart-durations" style="display: flex; flex-direction: column; gap: 12px;">
                                <!-- Rendered dynamically by JS -->
                            </div>
                        </div>
                    </div>

                    <!-- Definitive Treatment Performance Summary Table -->
                    <div class="research-card">
                        <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 8px;">
                            📋 ตารางสรุปผลการบรรลุเกณฑ์การรักษาจำเพาะ (Definitive Treatment Benchmarks Summary)
                        </div>
                        <div class="table-responsive">
                            <table class="research-table">
                                <thead>
                                    <tr>
                                        <th style="text-align: left;">กลุ่มโรคและหัตถการรักษาจำเพาะ</th>
                                        <th>เกณฑ์เป้าหมาย (Benchmark Standard)</th>
                                        <th>จำนวนเคสประเมิน (N)</th>
                                        <th>บรรลุเกณฑ์ n (%)</th>
                                        <th>หลุดเกณฑ์ n (%)</th>
                                        <th>เวลาจริงเฉลี่ย (Mean ± SD)</th>
                                        <th>มัธยฐาน [IQR]</th>
                                    </tr>
                                </thead>
                                <tbody id="prim-table-body">
                                    <!-- Rendered dynamically by JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ========================================== -->
                <!-- TAB 3: SECONDARY OBJECTIVE 01             -->
                <!-- ========================================== -->
                <div id="admin-tab-content-sec1" class="admin-tab-pane" style="display:none;">
                    <div class="research-banner" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #bbf7d0; border-left: 5px solid #16a34a;">
                        <div>
                            <div style="font-size: 11.5px; font-weight: 800; color: #15803d; letter-spacing: 0.5px; text-transform: uppercase;">
                                ⏱️ SECONDARY OBJECTIVE 01 • "Timeline & Benchmark Breaches"
                            </div>
                            <div style="font-size: 16px; font-weight: 700; color: #14532d; margin-top: 2px;">
                                Micro-Timeline Intervals & System Transfer Continuum
                            </div>
                            <div style="font-size: 12.5px; color: #15803d; opacity: 0.85; margin-top: 2px;">
                                To quantify the micro-timeline intervals (T1-5) and the overall transfer duration (TTotal) across the continuum.
                            </div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #bbf7d0; border-radius: 8px; padding: 8px 16px; text-align: right; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <div style="font-size: 11.5px; color: #64748b; font-weight: 600;">เวลารวมทั้งระบบเฉลี่ย (TTotal)</div>
                            <div id="sec1-mean-total" style="font-size: 26px; font-weight: 800; color: #0f766e; line-height: 1.1;">0 <span style="font-size: 14px; font-weight: 500;">นาที</span></div>
                            <div id="sec1-total-breach-badge" style="font-size: 11px; color: #dc2626;">ล่าช้าเกินเกณฑ์ 0%</div>
                        </div>
                    </div>

                    <!-- Stacked Continuum Visual Bar Card -->
                    <div class="research-card" style="margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
                            <div style="font-size: 14px; font-weight: 700; color: #1e3a8a;">
                                🛣️ แผนภูมิเส้นเวลาการส่งต่อต่อเนื่องตลอดสาย (Stacked Timeline Continuum across Transfer Stages)
                            </div>
                            <div id="sec1-bottleneck-badge" style="font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 999px; background: #fee2e2; color: #b91c1c;">
                                จุดคอขวดหลัก: กำลังประมวลผล...
                            </div>
                        </div>
                        <div style="font-size: 12px; color: #64748b; margin-bottom: 10px;">
                            แสดงสัดส่วนและค่าเฉลี่ยเวลาในแต่ละช่วงย่อย เพื่อระบุจุดคอขวดที่ทำให้เกิดความล่าช้าสูงสุดในการส่งต่อ
                        </div>
                        <!-- Stacked Bar Visual -->
                        <div id="sec1-stacked-bar-container" style="height: 36px; border-radius: 8px; overflow: hidden; display: flex; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); background: #e2e8f0; margin-bottom: 10px;">
                            <!-- Populated dynamically by JS -->
                        </div>
                        <!-- Segment Legend -->
                        <div id="sec1-stacked-legend" style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: #475569;">
                            <!-- Populated dynamically by JS -->
                        </div>
                    </div>

                    <!-- Micro-Interval Benchmark Breach Rates -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 14px; margin-bottom: 16px;">
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">
                                ⚠️ อัตราการเกิดความล่าช้าหลุดเกณฑ์ในแต่ละช่วงเวลา (% Benchmark Breaches)
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 10px;">
                                สัดส่วนเคสที่ใช้เวลาเกินเกณฑ์มาตรฐานในแต่ละช่วงรอยต่อของการส่งต่อ
                            </div>
                            <div id="sec1-breach-bars" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Populated dynamically by JS -->
                            </div>
                        </div>

                        <!-- Interval Micro-timeline Summary Table -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">
                                📋 สถิติพรรณนาช่วงเวลา Micro-Timeline (Descriptive Statistics)
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 10px;">
                                ค่าเฉลี่ย มัธยฐาน และอัตราการหลุดเกณฑ์เป้าหมายในแต่ละช่วง
                            </div>
                            <div class="table-responsive">
                                <table class="research-table">
                                    <thead>
                                        <tr>
                                            <th style="text-align: left;">ช่วงเวลา (Interval)</th>
                                            <th>เกณฑ์ (Benchmark)</th>
                                            <th>เฉลี่ย (Mean)</th>
                                            <th>มัธยฐาน [IQR]</th>
                                            <th>หลุดเกณฑ์ n (%)</th>
                                        </tr>
                                    </thead>
                                    <tbody id="sec1-table-body">
                                        <!-- Populated dynamically by JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ========================================== -->
                <!-- TAB 4: SECONDARY OBJECTIVE 02             -->
                <!-- ========================================== -->
                <div id="admin-tab-content-sec2" class="admin-tab-pane" style="display:none;">
                    <div class="research-banner" style="background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); border: 1px solid #fef08a; border-left: 5px solid #ca8a04;">
                        <div>
                            <div style="font-size: 11.5px; font-weight: 800; color: #a16207; letter-spacing: 0.5px; text-transform: uppercase;">
                                🔍 SECONDARY OBJECTIVE 02 • "Bottlenecks & Delay Triggers"
                            </div>
                            <div style="font-size: 16px; font-weight: 700; color: #713f12; margin-top: 2px;">
                                Patient, Operational & Maritime-Environmental Determinants
                            </div>
                            <div style="font-size: 12.5px; color: #854d0e; opacity: 0.85; margin-top: 2px;">
                                To identify patient, operational, and maritime-environmental determinants associated with referral delays.
                            </div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #fef08a; border-radius: 8px; padding: 8px 16px; text-align: right; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <div style="font-size: 11.5px; color: #64748b; font-weight: 600;">ปัจจัยความล่าช้าที่พบบ่อยสุด</div>
                            <div id="sec2-top-trigger-name" style="font-size: 15px; font-weight: 800; color: #b45309; line-height: 1.2;">กำลังวิเคราะห์...</div>
                            <div id="sec2-top-trigger-pct" style="font-size: 11.5px; color: #94a3b8;">พบใน 0% ของเคสทั้งหมด</div>
                        </div>
                    </div>

                    <!-- 3 Panels for 3 Determinant Domains -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-bottom: 16px;">
                        <!-- Domain 1: Patient Determinants -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>👤 1. ปัจจัยด้านผู้ป่วย (Patient Determinants)</span>
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                                ความรุนแรงของโรค ภาวะวิกฤต และความจำเป็นในการช่วยชีวิต
                            </div>
                            <div id="sec2-bars-patient" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Rendered dynamically by JS -->
                            </div>
                        </div>

                        <!-- Domain 2: Operational Determinants -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>⚙️ 2. ปัจจัยด้านการปฏิบัติการ (Operational Determinants)</span>
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                                รอบเวลาเดินแพ การปฏิบัติงานนอกเวลาปกติ และคิวสะสมท่าแพ
                            </div>
                            <div id="sec2-bars-operational" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Rendered dynamically by JS -->
                            </div>
                        </div>

                        <!-- Domain 3: Maritime-Environmental Determinants -->
                        <div class="research-card">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                <span>🌊 3. ปัจจัยทางทะเลและสภาพอากาศ (Maritime Determinants)</span>
                            </div>
                            <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                                ฤดูกาลมรสุม ระดับน้ำขึ้น-น้ำลง คลื่นลมทะเล และพายุฝน
                            </div>
                            <div id="sec2-bars-maritime" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Rendered dynamically by JS -->
                            </div>
                        </div>
                    </div>

                    <!-- Determinants Contrast: Delayed Cases vs On-Time Cases -->
                    <div class="research-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a;">
                                ⚖️ การเปรียบเทียบสัดส่วนปัจจัยขัดขวาง: กลุ่มส่งต่อล่าช้า (> 3 ชม.) vs กลุ่มส่งต่อทันเวลา (≤ 3 ชม.)
                            </div>
                            <span style="font-size: 11.5px; color: #64748b; font-weight: 500;">Delay Enrichment Analysis</span>
                        </div>
                        <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                            แสดงให้เห็นว่าปัจจัยใดมีความชุกสูงขึ้นอย่างชัดเจนในกลุ่มผู้ป่วยที่เกิดความล่าช้าเกินเกณฑ์มาตรฐาน
                        </div>
                        <div id="sec2-contrast-container" style="display: flex; flex-direction: column; gap: 10px;">
                            <!-- Rendered dynamically by JS -->
                        </div>
                    </div>
                </div>

                <!-- ========================================== -->
                <!-- TAB 5: SECONDARY OBJECTIVE 03             -->
                <!-- ========================================== -->
                <div id="admin-tab-content-sec3" class="admin-tab-pane" style="display:none;">
                    <div class="research-banner" style="background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); border: 1px solid #fbcfe8; border-left: 5px solid #db2777;">
                        <div>
                            <div style="font-size: 11.5px; font-weight: 800; color: #be185d; letter-spacing: 0.5px; text-transform: uppercase;">
                                📉 SECONDARY OBJECTIVE 03 • "Early Clinical Outcomes"
                            </div>
                            <div style="font-size: 16px; font-weight: 700; color: #831843; margin-top: 2px;">
                                Clinical Deterioration & Cohort Relative Risk Comparison
                            </div>
                            <div style="font-size: 12.5px; color: #9d174d; opacity: 0.85; margin-top: 2px;">
                                Evaluate the association of transfer delays with in-transit deterioration, Mainland ED death and 24-hour mortality. Compare cumulative incidence and relative risks between exposed and unexposed cohorts.
                            </div>
                        </div>
                    </div>

                    <!-- Cohort Breakdown KPI Cards -->
                    <div class="research-kpi-grid" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));">
                        <div class="research-card" style="border-left: 4px solid #1e40af;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">Inception Cohort ทั้งหมด (N)</div>
                            <div id="sec3-cohort-total" style="font-size: 26px; font-weight: 800; color: #1e40af; margin-top: 2px;">0</div>
                            <div style="font-size: 11.5px; color: #94a3b8;">ผู้ป่วยฉุกเฉินส่งต่อทั้งหมดในวิจัย</div>
                        </div>
                        <div class="research-card" style="border-left: 4px solid #dc2626;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">กลุ่มสัมผัสปัจจัยเสี่ยง (Exposed Cohort)</div>
                            <div id="sec3-cohort-exposed" style="font-size: 26px; font-weight: 800; color: #dc2626; margin-top: 2px;">0</div>
                            <div id="sec3-cohort-exposed-sub" style="font-size: 11.5px; color: #94a3b8;">0% • เผชิญความล่าช้า/อุปสรรควิกฤต</div>
                        </div>
                        <div class="research-card" style="border-left: 4px solid #16a34a;">
                            <div style="font-size: 12px; font-weight: 600; color: #64748b;">กลุ่มควบคุม (Unexposed / Control Cohort)</div>
                            <div id="sec3-cohort-unexposed" style="font-size: 26px; font-weight: 800; color: #16a34a; margin-top: 2px;">0</div>
                            <div id="sec3-cohort-unexposed-sub" style="font-size: 11.5px; color: #94a3b8;">0% • ส่งต่อทันเวลาตามมาตรฐาน</div>
                        </div>
                    </div>

                    <!-- Comparative Cumulative Incidence Bar Chart -->
                    <div class="research-card" style="margin-bottom: 14px;">
                        <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">
                            📊 การเปรียบเทียบอุบัติการณ์สะสมของผลลัพธ์ไม่พึงประสงค์ (Cumulative Incidence: Exposed vs Unexposed)
                        </div>
                        <div style="font-size: 11.5px; color: #64748b; margin-bottom: 12px;">
                            เปรียบเทียบร้อยละการเกิดผลลัพธ์ทางคลินิกระหว่างกลุ่ม Exposed (ล่าช้า) กับกลุ่ม Unexposed (ทันเวลา)
                        </div>
                        <div id="sec3-incidence-bars" style="display: flex; flex-direction: column; gap: 14px;">
                            <!-- Rendered dynamically by JS -->
                        </div>
                    </div>

                    <!-- 2x2 Contingency & Relative Risk Table -->
                    <div class="research-card" style="margin-bottom: 14px;">
                        <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 8px;">
                            📋 ตารางวิเคราะห์ความเสี่ยงเปรียบเทียบทางระบาดวิทยา (Epidemiological Risk Analysis: 2x2 Table & RR)
                        </div>
                        <div class="table-responsive">
                            <table class="research-table">
                                <thead>
                                    <tr>
                                        <th style="text-align: left;">ผลลัพธ์ทางคลินิก (Clinical Outcomes)</th>
                                        <th>Exposed Cohort<br><span style="font-weight: normal; font-size: 11px;">(n/N, Cumulative Inc.)</span></th>
                                        <th>Unexposed Cohort<br><span style="font-weight: normal; font-size: 11px;">(n/N, Cumulative Inc.)</span></th>
                                        <th>ความเสี่ยงสัมพัทธ์<br><span style="font-weight: normal; font-size: 11px;">Relative Risk (RR) [95% CI]</span></th>
                                        <th>ผลต่างความเสี่ยง<br><span style="font-weight: normal; font-size: 11px;">Risk Difference (ARR)</span></th>
                                        <th>การแปลผลทางคลินิก</th>
                                    </tr>
                                </thead>
                                <tbody id="sec3-risk-table-body">
                                    <!-- Rendered dynamically by JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Research Takeaway / Interpretation Box -->
                    <div id="sec3-takeaway-box" style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 5px solid #2563eb; border-radius: 8px; padding: 12px 18px;">
                        <div style="font-weight: 700; color: #1e3a8a; font-size: 13.5px; margin-bottom: 4px;">
                            💡 บทสรุปการวิเคราะห์ทางระบาดวิทยา (Epidemiological Interpretation Takeaway)
                        </div>
                        <div id="sec3-takeaway-text" style="font-size: 13px; color: #334155; line-height: 1.5;">
                            กำลังประมวลผลข้อมูลใน Cohort...
                        </div>
                    </div>
                </div>

            </div>

            <!-- Modal Footer -->
            <div style="padding: 10px 18px; background: #ffffff; border-top: 1px solid #cbd5e1; border-radius: 0 0 8px 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 12.5px; color: #64748b;">
                    💡 สามารถเลือกตัวกรอง Cohort ด้านบนเพื่อวิเคราะห์เจาะลึกเฉพาะกลุ่มโรค หรือส่งออก Excel / PDF สำหรับรายงานวิทยานิพนธ์ได้ทันที
                </div>
                <button type="button" class="btn btn-outline" onclick="closeAdminDashboard()" style="padding: 4px 12px; font-size: 13px;">
                    ปิดหน้าต่าง
                </button>
            </div>
        </div>
    </div>
    """
